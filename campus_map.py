# campus_map.py

import streamlit as st

# building data
buildings = [
    {"name": "Library", "lat": 33.881, "lon": -117.885},
    {"name": "Student Union", "lat": 33.882, "lon": -117.883},
    {"name": "Engineering Building", "lat": 33.883, "lon": -117.884},
]

st.title("Campus Map")

# extract names
building_names = [b["name"] for b in buildings]

# select building
selected_building = st.selectbox("Select Building", building_names)

# show selection
st.write(f"Selected: {selected_building}")

# show map (IMPORTANT for tests)
st.map(
    [{"lat": b["lat"], "lon": b["lon"]} for b in buildings]
)
