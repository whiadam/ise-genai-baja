# use AI for templating
import streamlit as st
from .landing_page import render_landing_page

def display_flyer_updater_page():
    tab1, tab2 = st.tabs(["Upload a Photo", "Flyer Log"])

    with tab1:
        render_landing_page()
    with tab2:
        st.write("PLACEHOLDER LOG")
