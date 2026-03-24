#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from alerts_module.alerts import display_alerts
from flyer_updater.view import display_flyer_updater_page
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = 'user1'
def register_pages():
   """Put modules(pages)in the return statement  here"""
   return[
           st.Page(display_app_page, title = "Home", default= True),
           st.Page(display_flyer_updater_page, title ="Flyer Updater"),
           # NEW MODULES(pages) GO HERE vvvvvvvvv
            ]

def display_app_page():
    """Displays the home page of the app."""
    st.title("Campus Info App")

    profile = get_user_profile(userId)
    st.caption(f"Logged in as @{profile['username']}")

    st.divider()

    # Example events list (later this can come from the Create Events module) 
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


# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    nav = st.navigation(register_pages())
    nav.run()
