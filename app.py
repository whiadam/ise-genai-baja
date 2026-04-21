#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################
import streamlit as st

def register_pages():
    """Put modules(pages) in the return statement here"""
    return [
        st.Page("campus_map.py", title="Campus Map", default = True),
        st.Page("campus_info_dashboard.py", title="Dashboard"),
        st.Page("flyer_updater/flyer_view.py", title="Flyer Updater"),
        st.Page("campus_voice.py", title="Campus Voice"),
        st.Page("alerts_module/alerts_view.py"   , title="Alerts"),
        st.Page("event_module/view.py", title="Events"),
    ]
if __name__ == '__main__':
    nav = st.navigation(register_pages())
    nav.run()
