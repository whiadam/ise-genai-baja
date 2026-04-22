#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################
import streamlit as st
st.set_page_config(
    page_title="Duke Campus",
    initial_sidebar_state="expanded",
    page_icon="./custom_components/duke.png"
)

st.html("""
<style>
    [data-testid="stSidebar"] a {
        font-size: 16px !important;
        font-weight: 400;
    }
    
    [data-testid="stSidebar"] a:hover,
    [data-testid="stSidebar"] a:focus,
    a[aria-current="page"]{
        font-size: 24px  !important;
        font-weight: 700;
    }
</style>
""")
def register_pages():
    """Put modules(pages) in the return statement here"""
    return [
        st.Page("campus_map.py", title="Campus Map", default = True),
        st.Page("campus_info_dashboard.py", title="Dashboard"),
        st.Page("flyer_updater/flyer_view.py", title="Event Creation Agent"),
        st.Page("campus_voice.py", title="Campus Voice"),
        st.Page("alerts_module/alerts_view.py"   , title="Alerts"),
        st.Page("event_module/view.py", title="Events"),
    ]
if __name__ == '__main__':
    nav = st.navigation(register_pages())
    nav.run()
