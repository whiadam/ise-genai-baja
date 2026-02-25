#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################
from __future__ import annotations  
from datetime import datetime, date, time, timedelta  
from typing import Any  

import streamlit as st 
from internals import create_component


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


# Danae's section (add other sections above or below mine)
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

    # =======================
    # Top Notification Banner
    # =======================
    enabled_alerts = [a for a in st.session_state["alerts"] if a.get("enabled", True)]
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
                st.warning(f"Alert: **{next_alert['title']}** triggers in **{mins} min** at {next_time.strftime('%I:%M %p')}")
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
            title = st.text_input("Alert Title")
            category = st.selectbox("Category", ["Academic", "Dining", "Sports", "Social", "Safety", "Other"])
            alert_type = st.selectbox("Alert Type", ["Event Reminder", "Personal Reminder", "Campus Announcement"])

            minutes_before = None
            remind_at = None
            event_start = None
            event_name = None

            if alert_type == "Event Reminder":
                before = st.selectbox("Notify", ["5 min", "15 min", "30 min", "1 hour", "1 day"])
                minutes_before = {"5 min": 5, "15 min": 15, "30 min": 30, "1 hour": 60, "1 day": 1440}[before]
                event_options = ["(none)"] + [e.get("name", "Untitled event") for e in events]
                chosen = st.selectbox("Link to Event (optional)", event_options)
                if chosen != "(none)":
                    idx = event_options.index(chosen) - 1
                    event_name = events[idx].get("name")
                    event_start = events[idx].get("start")
                d = st.date_input("Event Date", value=date.today())
                t = st.time_input("Event Start Time", value=time(18, 0))
                if event_start is None:
                    event_start = _parse_dt(d, t)

            if alert_type == "Personal Reminder":
                d = st.date_input("Reminder Date", value=date.today())
                t = st.time_input("Reminder Time", value=time(18, 0))
                remind_at = _parse_dt(d, t)

            st.markdown("**Delivery Methods**")
            in_app = st.checkbox("In-app banner", value=True)
            email = st.checkbox("Email (future)")
            sms = st.checkbox("SMS (future)")

            submit = st.form_submit_button("Save Alert")

        if submit:
            if not title.strip():
                st.error("Alert title required.")
            else:
                st.session_state["alerts"].append({
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
                })
                st.session_state["next_alert_id"] += 1
                st.success("Alert created!")

    # =======================
    # Active Alerts
    # =======================
    with col_right:
        st.markdown("### Active Alerts")

        active = [a for a in st.session_state["alerts"] if a.get("enabled", True)]
        if not active:
            st.info("No active alerts yet.")

        for a in list(st.session_state["alerts"]):
            if not a.get("enabled", True):
                continue

            trigger = _compute_trigger_time(a)
            trigger_str = trigger.strftime("%a %I:%M %p") if trigger else "N/A"

            with st.container(border=True):
                st.markdown(f"**{a['title']}**")
                st.write(f"{a['category']} • {a['alert_type']}")
                st.write(f"Next trigger: {trigger_str}")

                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("Edit", key=f"edit_{a['id']}"):
                        st.session_state["editing_alert_id"] = a["id"]
                        st.rerun()
                with c2:
                    if st.button("Disable", key=f"disable_{a['id']}"):
                        a["enabled"] = False
                        st.rerun()
                with c3:
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
                    new_title = st.text_input("Alert Title", value=target["title"])
                    new_category = st.selectbox("Category", ["Academic", "Dining", "Sports", "Social", "Safety", "Other"],
                                                index=["Academic", "Dining", "Sports", "Social", "Safety", "Other"].index(target["category"]))
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
            category_filter = st.selectbox("Filter", ["All", "Academic", "Dining", "Sports", "Social", "Safety", "Other"])
        with scol:
            q = st.text_input("Search alerts")

        rows = []
        for tt, a in upcoming_pairs:
            if category_filter != "All" and a["category"] != category_filter:
                continue
            if q and q.lower() not in a["title"].lower():
                continue
            source = "Events" if a.get("event_name") else ("Personal" if a["alert_type"] == "Personal Reminder" else "System")
            rows.append({"Time": tt.strftime("%I:%M %p"), "Alert": a["title"], "Source": source})

        if rows:
            st.dataframe(rows, hide_index=True, use_container_width=True)
        else:
            st.write("No upcoming alerts match your filters.")
