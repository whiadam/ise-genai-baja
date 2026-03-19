# campus_map.py

import streamlit as st
import pandas as pd

st.title("Campus Map")

# building data (NO "None" in map data)
buildings = [
    {"name": "Library", "lat": 33.881, "lon": -117.885, "type": "study"},
    {"name": "Student Union", "lat": 33.882, "lon": -117.883, "type": "social"},
    {"name": "Engineering Building", "lat": 33.883, "lon": -117.884, "type": "academic"},
    {"name": "Gym", "lat": 33.884, "lon": -117.882, "type": "fitness"},
    {"name": "Cafeteria", "lat": 33.885, "lon": -117.881, "type": "food"},
]

# sidebar selectbox MUST include "None"
building_names = ["None"] + [b["name"] for b in buildings]
selected = st.sidebar.selectbox("Select Building", building_names, index=0)

# THIS PART IS CRITICAL 👇
map_data = pd.DataFrame(buildings)[["lat", "lon"]]

# Use st.map EXACTLY like this
st.map(map_data)

# selection logic
for b in buildings:
    if b["name"] == selected:
        st.success(f"Selected: {b['name']} ({b['type']})")
