#################### Imports #####################################
from __future__ import annotations
from datetime import datetime, date, time, timedelta
from typing import Any

import streamlit as st
from .alerts_fetcher import get_all_alerts

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


def _parse_dt(d: date, t: time) -> datetime:
    """
    Combines date + time into a datetime.

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    return datetime(d.year, d.month, d.day, t.hour, t.minute, 0)


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
        return datetime.now()

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
                alert_time = datetime.fromisoformat(alert_time.replace("Z", ""))
            except ValueError:
                alert_time = datetime.now()

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


def display_alerts(user_id: str = "user1", events: list[dict[str, Any]] | None = None) -> None:
    """
    Displays and manages alerts for the Campus Info App.

    Sections:
    - Top notification banner
    - Create alert + settings
    - Active alerts (edit / disable / delete)
    - Upcoming alerts (filter + search)

    Lines vibe-coded with GPT-5.2 Thinking.
    """
    _ensure_alert_state()
    events = events or []
    now = datetime.now()

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
    for a in enabled_alerts:
        tt = _compute_trigger_time(a)
        if tt and tt >= now:
            upcoming_pairs.append((tt, a))
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
                        "created_at": datetime.now(),
                        "source": "local",
                        "alert_description": None,
                        "event_id": None,
                    }
                )
                st.session_state["next_alert_id"] += 1
                st.success("Alert created!")

    # =======================
    # Active Alerts
    # =======================
    with col_right:
        st.markdown("### Active Alerts")

        active = [a for a in all_alerts if a.get("enabled", True)]
        if not active:
            st.info("No active alerts yet.")

        for a in list(all_alerts):
            if not a.get("enabled", True):
                continue

            trigger = _compute_trigger_time(a)
            trigger_str = trigger.strftime("%a %I:%M %p") if trigger else "N/A"

            with st.container(border=True):
                st.markdown(f"**{a['title']}**")
                st.write(f"{a['category']} • {a['alert_type']}")
                st.write(f"Next trigger: {trigger_str}")

                if a.get("alert_description"):
                    st.write(f"Description: {a['alert_description']}")

                if a.get("event_id") is not None:
                    st.write(f"Event ID: {a['event_id']}")

                c1, c2, c3 = st.columns(3)
                is_database_alert = str(a["id"]).startswith("db_")

                with c1:
                    if is_database_alert:
                        st.button("Edit", key=f"edit_{a['id']}", disabled=True)
                    else:
                        if st.button("Edit", key=f"edit_{a['id']}"):
                            st.session_state["editing_alert_id"] = a["id"]
                            st.rerun()

                with c2:
                    if is_database_alert:
                        st.button("Disable", key=f"disable_{a['id']}", disabled=True)
                    else:
                        if st.button("Disable", key=f"disable_{a['id']}"):
                            a["enabled"] = False
                            st.rerun()

                with c3:
                    if is_database_alert:
                        st.button("Delete", key=f"delete_{a['id']}", disabled=True)
                    else:
                        if st.button("Delete", key=f"delete_{a['id']}"):
                            st.session_state["alerts"].remove(a)
                            st.rerun()

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
        for tt, a in upcoming_pairs:
            if category_filter != "All" and a["category"] != category_filter:
                continue
            if q and q.lower() not in a["title"].lower():
                continue
            source = "Events" if a.get("event_name") else ("Personal" if a["alert_type"] == "Personal Reminder" else "System")
            rows.append({"Time": tt.strftime("%I:%M %p"), "Alert": a["title"], "Source": source})

        if rows:
            st.dataframe(rows, hide_index=True, width="stretch")
        else:
            st.write("No upcoming alerts match your filters.")

################## End of Danae's Section ########################
