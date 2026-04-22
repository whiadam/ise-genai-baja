#################### Imports #####################################
from __future__ import annotations
from datetime import datetime, date, time, timedelta, timezone
from typing import Any

import streamlit as st
try:
    from .alerts_fetcher import get_all_alerts, get_genai_alert_summary
except ImportError:
    from alerts_fetcher import get_all_alerts, get_genai_alert_summary

##################### Danae's Section ############################
def _ensure_alert_state() -> None:
    """
    Ensures Streamlit session state has the keys needed for alerts.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    if "alerts" not in st.session_state:
        st.session_state["alerts"] = []
    if "next_alert_id" not in st.session_state:
        st.session_state["next_alert_id"] = 1
    if "dismissed_banner_ids" not in st.session_state:
        st.session_state["dismissed_banner_ids"] = set()
    if "editing_alert_id" not in st.session_state:
        st.session_state["editing_alert_id"] = None
    if "active_alert_index" not in st.session_state:
        st.session_state["active_alert_index"] = 0
    if "alert_summary" not in st.session_state:
        st.session_state["alert_summary"] = None


def _parse_dt(d: date, t: time) -> datetime:
    """
    Combines date + time into a datetime.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    return datetime(d.year, d.month, d.day, t.hour, t.minute, 0, tzinfo=timezone.utc)


def _compute_trigger_time(alert: dict[str, Any]) -> datetime | None:
    """
    Computes the next trigger time for an alert.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    if not alert.get("enabled", True):
        return None

    alert_type = alert.get("alert_type")

    if alert_type == "Personal Reminder":
        return alert.get("remind_at")

    if alert_type == "Event Reminder":
        event_start = alert.get("event_start")
        minutes_before = int(alert.get("minutes_before", 60))
        if event_start is None:
            return None
        return event_start - timedelta(minutes=minutes_before)

    if alert_type == "Campus Announcement":
        return datetime.now(timezone.utc)

    return None


def _normalize_bigquery_alerts(bigquery_alerts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Converts BigQuery alert rows into the format used by display_alerts.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    normalized_alerts = []

    for alert in bigquery_alerts:
        preferences = alert.get("preference", [])
        alert_time = alert.get("time_of_alert")

        if isinstance(alert_time, str):
            try:
                alert_time = datetime.fromisoformat(alert_time.replace("Z", "+00:00"))
            except ValueError:
                alert_time = datetime.now(timezone.utc)

        if "Email" in preferences or "Text" in preferences:
            category = "Academic"
        elif "None" in preferences:
            category = "Other"
        else:
            category = "Other"

        normalized_alerts.append(
            {
                "id": f"db_{alert['alert_id']}",
                "user_id": "database_user",
                "title": alert.get("alert_name", "Untitled Alert"),
                "category": category,
                "alert_type": "Personal Reminder" if alert.get("reoccuring") else "Campus Announcement",
                "minutes_before": None,
                "event_start": None,
                "event_name": f"Event {alert['event_id']}" if alert.get("event_id") is not None else None,
                "remind_at": alert_time,
                "delivery": {
                    "in_app": True,
                    "email": "Email" in preferences,
                    "sms": "Text" in preferences,
                },
                "enabled": True,
                "created_at": alert_time,
                "source": "database",
                "alert_description": alert.get("alert_description"),
                "event_id": alert.get("event_id"),
            }
        )

    return normalized_alerts


def _get_urgent_alert_index(active_alerts: list[dict[str, Any]]) -> int:
    """
    Finds the index of the alert with the earliest trigger time.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    urgent_index = 0
    earliest_time = None

    for i, alert in enumerate(active_alerts):
        trigger_time = _compute_trigger_time(alert)
        if trigger_time is not None and (earliest_time is None or trigger_time < earliest_time):
            earliest_time = trigger_time
            urgent_index = i

    return urgent_index


def _render_active_alert_card(alert: dict[str, Any]) -> None:
    """
    Renders a single active alert card.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    trigger = _compute_trigger_time(alert)
    trigger_str = trigger.strftime("%a %I:%M %p") if trigger else "N/A"

    with st.container(border=True):
        st.markdown(f"**{alert['title']}**")
        st.write(f"{alert['category']} • {alert['alert_type']}")
        st.write(f"Next trigger: {trigger_str}")

        if alert.get("alert_description"):
            st.write(f"Description: {alert['alert_description']}")

        if alert.get("event_id") is not None:
            st.write(f"Event ID: {alert['event_id']}")

        c1, c2, c3 = st.columns(3)
        is_database_alert = str(alert["id"]).startswith("db_")

        with c1:
            if is_database_alert:
                st.button("Edit", key=f"edit_{alert['id']}", disabled=True)
            else:
                if st.button("Edit", key=f"edit_{alert['id']}"):
                    st.session_state["editing_alert_id"] = alert["id"]
                    st.rerun()

        with c2:
            if is_database_alert:
                st.button("Disable", key=f"disable_{alert['id']}", disabled=True)
            else:
                if st.button("Disable", key=f"disable_{alert['id']}"):
                    alert["enabled"] = False
                    st.rerun()

        with c3:
            if is_database_alert:
                st.button("Delete", key=f"delete_{alert['id']}", disabled=True)
            else:
                if st.button("Delete", key=f"delete_{alert['id']}"):
                    st.session_state["alerts"].remove(alert)
                    st.rerun()


def _render_smart_summary() -> None:
    """
    Renders the GenAI smart summary section.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    st.markdown("### Smart Alert Summary")
    st.caption("AI-generated overview of your current alerts")

    summary_col, button_col = st.columns([3, 1])

    with button_col:
        refresh_summary = st.button("🔄 Refresh Summary", key="refresh_summary", use_container_width=True)

    if refresh_summary:
        with st.spinner("Generating smart summary..."):
            try:
                st.session_state["alert_summary"] = get_genai_alert_summary()
            except Exception as e:
                st.session_state["alert_summary"] = f"Error generating summary: {e}"

    with summary_col:
        if st.session_state["alert_summary"]:
            st.info(st.session_state["alert_summary"])
        else:
            st.write("Click **Refresh Summary** to generate an AI overview of your alerts.")


def display_alerts(user_id: str = "user1", events: list[dict[str, Any]] | None = None) -> None:
    """
    Displays and manages alerts for the Campus Info App.

    Sections:
    - Top notification banner
    - Smart alert summary
    - Create alert + settings
    - Active alerts carousel
    - Edit alert
    - Upcoming alerts (filter + search)

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    _ensure_alert_state()
    events = events or []
    now = datetime.now(timezone.utc)

    try:
        bigquery_alerts = get_all_alerts()
        database_alerts = _normalize_bigquery_alerts(bigquery_alerts)
    except Exception as e:
        st.warning(f"Could not load alerts from BigQuery: {e}")
        database_alerts = []

    local_alerts = st.session_state["alerts"]
    all_alerts = database_alerts + local_alerts

    # =======================
    # Top Notification Banner
    # =======================
    enabled_alerts = [a for a in all_alerts if a.get("enabled", True)]
    upcoming_pairs = []
    for alert in enabled_alerts:
        trigger_time = _compute_trigger_time(alert)
        if trigger_time and trigger_time >= now:
            upcoming_pairs.append((trigger_time, alert))
    upcoming_pairs.sort(key=lambda x: x[0])

    if upcoming_pairs:
        next_time, next_alert = upcoming_pairs[0]
        next_id = next_alert["id"]

        if next_id not in st.session_state["dismissed_banner_ids"]:
            mins = int((next_time - now).total_seconds() // 60)
            left, mid, right = st.columns([1, 8, 1])
            with left:
                st.write("🔔")
            with mid:
                st.warning(
                    f"Alert: **{next_alert['title']}** triggers in **{mins} min** at {next_time.strftime('%I:%M %p')}"
                )
            with right:
                if st.button("✕", key=f"dismiss_{next_id}"):
                    st.session_state["dismissed_banner_ids"].add(next_id)
                    st.rerun()

    st.subheader("Alerts")

    # =======================
    # Smart Alert Summary
    # =======================
    _render_smart_summary()

    col_left, col_right = st.columns(2)

    # =======================
    # Create Alert + Settings
    # =======================
    with col_left:
        st.markdown("### Create an Alert")

        with st.form("create_alert_form", clear_on_submit=True):
            title = st.text_input("Alert Title", key="alerts_title_input")
            category = st.selectbox(
                "Category",
                ["Academic", "Dining", "Sports", "Social", "Safety", "Other"],
                key="alerts_category_select",
            )
            alert_type = st.selectbox(
                "Alert Type",
                ["Event Reminder", "Personal Reminder", "Campus Announcement"],
                key="alerts_type_select",
            )

            minutes_before = None
            remind_at = None
            event_start = None
            event_name = None

            if alert_type == "Event Reminder":
                before = st.selectbox(
                    "Notify",
                    ["5 min", "15 min", "30 min", "1 hour", "1 day"],
                    key="alerts_notify_select",
                )
                minutes_before = {"5 min": 5, "15 min": 15, "30 min": 30, "1 hour": 60, "1 day": 1440}[before]

                event_options = ["(none)"] + [e.get("name", "Untitled event") for e in events]
                chosen = st.selectbox("Link to Event (optional)", event_options, key="alerts_link_event_select")

                if chosen != "(none)":
                    idx = event_options.index(chosen) - 1
                    event_name = events[idx].get("name")
                    event_start = events[idx].get("start")

                d = st.date_input("Event Date", value=date.today(), key="alerts_event_date")
                t = st.time_input("Event Start Time", value=time(18, 0), key="alerts_event_time")

                if event_start is None:
                    event_start = _parse_dt(d, t)

            if alert_type == "Personal Reminder":
                d = st.date_input("Reminder Date", value=date.today(), key="alerts_reminder_date")
                t = st.time_input("Reminder Time", value=time(18, 0), key="alerts_reminder_time")
                remind_at = _parse_dt(d, t)

            st.markdown("**Delivery Methods**")
            in_app = st.checkbox("In-app banner", value=True, key="alerts_delivery_in_app")
            email = st.checkbox("Email (future)", key="alerts_delivery_email")
            sms = st.checkbox("SMS (future)", key="alerts_delivery_sms")

            submit = st.form_submit_button("Save Alert")

        if submit:
            if not title.strip():
                st.error("Alert title required.")
            else:
                st.session_state["alerts"].append(
                    {
                        "id": st.session_state["next_alert_id"],
                        "user_id": user_id,
                        "title": title.strip(),
                        "category": category,
                        "alert_type": alert_type,
                        "minutes_before": minutes_before,
                        "event_start": event_start,
                        "event_name": event_name,
                        "remind_at": remind_at,
                        "delivery": {"in_app": in_app, "email": email, "sms": sms},
                        "enabled": True,
                        "created_at": datetime.now(timezone.utc),
                        "source": "local",
                        "alert_description": None,
                        "event_id": None,
                    }
                )
                st.session_state["next_alert_id"] += 1
                st.success("Alert created!")

    # =======================
    # Active Alerts Carousel
    # =======================
    with col_right:
        st.markdown("### Active Alerts")

        active = [a for a in all_alerts if a.get("enabled", True)]
        if not active:
            st.info("No active alerts yet.")
        else:
            if st.session_state["active_alert_index"] >= len(active):
                st.session_state["active_alert_index"] = 0

            nav_left, nav_center, nav_right = st.columns([1, 2, 1])

            with nav_left:
                if st.button("⬅", key="alerts_prev_card", use_container_width=True):
                    st.session_state["active_alert_index"] = (
                        st.session_state["active_alert_index"] - 1
                    ) % len(active)
                    st.rerun()

            with nav_center:
                current_index = st.session_state["active_alert_index"]
                st.markdown(
                    f"<div style='text-align: center; padding-top: 0.5rem;'><strong>"
                    f"Alert {current_index + 1} of {len(active)}"
                    f"</strong></div>",
                    unsafe_allow_html=True,
                )

            with nav_right:
                if st.button("➡", key="alerts_next_card", use_container_width=True):
                    st.session_state["active_alert_index"] = (
                        st.session_state["active_alert_index"] + 1
                    ) % len(active)
                    st.rerun()

            urgent_index = _get_urgent_alert_index(active)
            if st.button("⚡ Jump to Urgent", key="alerts_jump_urgent", use_container_width=True):
                st.session_state["active_alert_index"] = urgent_index
                st.rerun()

            current_alert = active[st.session_state["active_alert_index"]]
            _render_active_alert_card(current_alert)

        # =======================
        # Edit Alert
        # =======================
        edit_id = st.session_state.get("editing_alert_id")
        if edit_id is not None:
            target = next((x for x in st.session_state["alerts"] if x["id"] == edit_id), None)
            if target:
                st.markdown("### Edit Alert")
                with st.form(f"edit_form_{edit_id}"):
                    new_title = st.text_input("Alert Title", value=target["title"], key=f"alerts_edit_title_{edit_id}")
                    new_category = st.selectbox(
                        "Category",
                        ["Academic", "Dining", "Sports", "Social", "Safety", "Other"],
                        index=["Academic", "Dining", "Sports", "Social", "Safety", "Other"].index(target["category"]),
                        key=f"alerts_edit_category_{edit_id}",
                    )
                    save_edit = st.form_submit_button("Save Changes")

                if save_edit:
                    target["title"] = new_title.strip() or target["title"]
                    target["category"] = new_category
                    st.session_state["editing_alert_id"] = None
                    st.rerun()

        # =======================
        # Upcoming Alerts
        # =======================
        st.markdown("### Upcoming Alerts")
        fcol, scol = st.columns([1, 2])
        with fcol:
            category_filter = st.selectbox(
                "Filter",
                ["All", "Academic", "Dining", "Sports", "Social", "Safety", "Other"],
                key="alerts_upcoming_filter",
            )
        with scol:
            q = st.text_input("Search alerts", key="alerts_upcoming_search")

        rows = []
        for trigger_time, alert in upcoming_pairs:
            if category_filter != "All" and alert["category"] != category_filter:
                continue
            if q and q.lower() not in alert["title"].lower():
                continue
            source = "Events" if alert.get("event_name") else ("Personal" if alert["alert_type"] == "Personal Reminder" else "System")
            rows.append({"Time": trigger_time.strftime("%I:%M %p"), "Alert": alert["title"], "Source": source})

        if rows:
            st.dataframe(rows, hide_index=True, width="stretch")
        else:
            st.write("No upcoming alerts match your filters.")

################## End of Danae's Section ########################