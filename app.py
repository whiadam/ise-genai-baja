#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from alerts_module.alerts import display_alerts
from flyer_updater.flyer_view import display_flyer_updater_page
from data_fetcher import get_active_polls, get_issues, get_genai_data

userId = 'user1'


def register_pages():
    """Put modules(pages) in the return statement here"""
    return [
        st.Page(display_app_page, title="Home", default=True),
        st.Page(display_flyer_updater_page, title="Flyer Updater"),
        st.Page("campus_voice.py", title="Campus Voice"),
        st.Page(display_alerts, title ="Alerts")
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


if __name__ == '__main__':
    nav = st.navigation(register_pages())
    nav.run()
