# use AI for templating
import streamlit as st
from landing_page import render_landing_page
tab1, tab2 = st.tabs(["Upload a Photo", "Flyer Log"])

with tab1:
    render_landing_page()

