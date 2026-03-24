#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from alerts_module.alerts import display_alerts
from flyer_updater.view import display_flyer_updater_page
from data_fetcher import get_active_polls, get_issues, get_genai_data

userId = 'user1'


def register_pages():
    """Put modules(pages) in the return statement here"""
    return [
        st.Page(display_app_page, title="Home", default=True),
        st.Page(display_flyer_updater_page, title="Flyer Updater"),
        st.Page("campus_voice.py", title="Campus Voice"),
    ]


def display_app_page():
    """Displays the home page of the app."""
    st.title("Campus Info App")

    # ✅ FIXED (no more profile error)
    st.caption("Logged in as student user")

    st.divider()

    # ✅ Show some data from your database
    polls = get_active_polls()
    issues = get_issues()

    st.subheader("Quick Poll Preview")
    if polls:
        for poll in polls[:3]:
            st.write(f"- {poll['poll_question']}")
    else:
        st.write("No active polls right now.")

    st.subheader("Recent Issues Preview")
    if issues:
        for issue in issues[:3]:
            st.write(f"- {issue['title']}")
    else:
        st.write("No recent issues right now.")

    # ✅ GenAI button
    if st.button("Generate AI Summary"):
        summary = get_genai_data(userId)
        st.write(summary["content"])

    # Existing alerts system (leave this)
    example_events = [
        {"name": "Dining Hall Special", "start": st.session_state.get("demo_event_start")},
    ]

    if example_events[0]["start"] is None:
        default_start = st.session_state.get("demo_event_start_default")
        computed_start = (
            __import__("datetime").datetime.now()
            .replace(second=0, microsecond=0)
            + __import__("datetime").timedelta(hours=2)
        )
        st.session_state["demo_event_start"] = default_start or computed_start
        example_events[0]["start"] = st.session_state["demo_event_start"]

    display_alerts(user_id=userId, events=example_events)


if __name__ == '__main__':
    nav = st.navigation(register_pages())
    nav.run()