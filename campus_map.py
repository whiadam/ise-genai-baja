# campus_map.py

import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("Campus Map")

# building data (exactly 5)
buildings = [
    {"name": "Library", "lat": 33.881, "lon": -117.885, "type": "study"},
    {"name": "Student Union", "lat": 33.882, "lon": -117.883, "type": "social"},
    {"name": "Engineering Building", "lat": 33.883, "lon": -117.884, "type": "academic"},
    {"name": "Gym", "lat": 33.884, "lon": -117.882, "type": "fitness"},
    {"name": "Cafeteria", "lat": 33.885, "lon": -117.881, "type": "food"},
]

# sidebar selectbox (must start with None)
building_names = ["None"] + [b["name"] for b in buildings]
selected = st.sidebar.selectbox("Select Building", building_names, index=0)

# create dataframe
df = pd.DataFrame(buildings)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_radius=100,
)

view_state = pdk.ViewState(
    latitude=33.882,
    longitude=-117.884,
    zoom=15,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
)

st.pydeck_chart(deck)

# selection logic
for b in buildings:
    if b["name"] == selected:
        st.success(f"Selected: {b['name']} ({b['type']})")
