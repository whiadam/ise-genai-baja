#############################################################################
# event_module/view.py
#
# Streamlit page — lists upcoming campus events and lets staff create new
# ones.  All data lives in BigQuery via event_fetcher.py.
#############################################################################

import streamlit as st
from datetime import datetime
from event_module.event_fetcher import get_upcoming_events, get_events, create_event
from event_module.event import Event

st.title("📅 Campus Events")

tab_view, tab_create = st.tabs(["Upcoming Events", "Create Event"])

# ---------------------------------------------------------------------------
# Tab 1 — view events
# ---------------------------------------------------------------------------
with tab_view:
    st.subheader("Upcoming Events")
    try:
        events = get_upcoming_events()
    except Exception as e:
        st.error(f"Could not load events: {e}")
        events = []

    if not events:
        st.info("No upcoming events scheduled. Check back soon!")
    else:
        for event in events:
            with st.container(border=True):
                col_info, col_meta = st.columns([3, 1])
                with col_info:
                    st.markdown(f"### {event.event_title or 'Untitled Event'}")
                    if event.description:
                        st.write(event.description)
                    if event.event_location:
                        st.write(f"📍 {event.event_location}")
                with col_meta:
                    if event.event_startime:
                        st.metric("Starts", event.event_startime.strftime("%b %d, %I:%M %p"))
                    if event.event_endtime:
                        st.caption(f"Ends: {event.event_endtime.strftime('%I:%M %p')}")
                    if event.department:
                        st.caption(f"Dept: {event.department}")

# ---------------------------------------------------------------------------
# Tab 2 — create event
# ---------------------------------------------------------------------------
with tab_create:
    st.subheader("Create a New Event")
    with st.form("create_event_form", clear_on_submit=True):
        title    = st.text_input("Event Title *")
        desc     = st.text_area("Description")
        location = st.text_input("Location")
        dept     = st.text_input("Department")
        creator  = st.text_input("Your Name *")

        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start Date")
            start_time = st.time_input("Start Time")
        with col_end:
            end_date = st.date_input("End Date")
            end_time = st.time_input("End Time")

        submitted = st.form_submit_button("Create Event")

    if submitted:
        if not title.strip() or not creator.strip():
            st.error("Event Title and Your Name are required.")
        else:
            new_event = Event(
                time_created    = datetime.utcnow(),
                creator         = creator.strip(),
                event_title     = title.strip(),
                description     = desc.strip() or None,
                event_location  = location.strip() or None,
                department      = dept.strip() or None,
                event_startime  = datetime.combine(start_date, start_time),
                event_endtime   = datetime.combine(end_date, end_time),
            )
            try:
                event_id = create_event(new_event)
                st.success(f"Event created! ID: {event_id}")
            except Exception as e:
                st.error(f"Failed to create event: {e}")
