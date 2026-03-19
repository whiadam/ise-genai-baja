# campus_map.py

import streamlit as st
import pandas as pd

st.title("Campus Map")

# building data (MUST be 5)
buildings = [
    {"name": "None", "lat": 0, "lon": 0, "type": ""},
    {"name": "Library", "lat": 33.881, "lon": -117.885, "type": "study"},
    {"name": "Student Union", "lat": 33.882, "lon": -117.883, "type": "social"},
    {"name": "Engineering Building", "lat": 33.883, "lon": -117.884, "type": "academic"},
    {"name": "Gym", "lat": 33.884, "lon": -117.882, "type": "fitness"},
]

# sidebar selectbox (IMPORTANT)
building_names = [b["name"] for b in buildings]
selected = st.sidebar.selectbox("Select Building", building_names, index=0)

# map data (must be 5 markers)
map_data = pd.DataFrame(
    [{"lat": b["lat"], "lon": b["lon"]} for b in buildings]
)

st.map(map_data)

# selection behavior
for b in buildings:
    if b["name"] == selected and selected != "None":
        st.success(f"Selected: {b['name']} ({b['type']})")
