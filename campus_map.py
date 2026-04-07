#############################################################################
# campus_map.py
#
# Interactive campus map using Folium + streamlit-folium.
# Buildings are defined here as static data; swap in a BigQuery fetch
# (similar to get_active_polls in data_fetcher.py) whenever the DB table
# is ready.
#############################################################################

import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# ---------------------------------------------------------------------------
# Duke University campus center  (~36.0015° N, 78.9391° W)
# ---------------------------------------------------------------------------
CAMPUS_CENTER = [36.001465, -78.939133]

# ---------------------------------------------------------------------------
# Building data — Duke University West Campus landmarks
# ---------------------------------------------------------------------------
BUILDINGS = [
    {"id": 1,  "name": "Perkins & Bostock Libraries", "lat": 36.0019, "lon": -78.9388, "type": "study"},
    {"id": 2,  "name": "Bryan Center",                "lat": 36.0009, "lon": -78.9410, "type": "dining"},
    {"id": 3,  "name": "Wilson Recreation Center",    "lat": 36.0005, "lon": -78.9440, "type": "recreation"},
    {"id": 4,  "name": "Fitzpatrick Center (CIEMAS)", "lat": 36.0017, "lon": -78.9430, "type": "academic"},
    {"id": 5,  "name": "Duke Chapel",                 "lat": 36.0007, "lon": -78.9389, "type": "academic"},
    {"id": 6,  "name": "Allen Building",              "lat": 36.0004, "lon": -78.9376, "type": "admin"},
    {"id": 7,  "name": "Bryan Center Parking Garage", "lat": 36.0006, "lon": -78.9420, "type": "parking"},
    {"id": 8,  "name": "Cameron Indoor Stadium",      "lat": 35.9979, "lon": -78.9420, "type": "recreation"},
    {"id": 9,  "name": "Nasher Museum of Art",        "lat": 36.0033, "lon": -78.9406, "type": "academic"},
    {"id": 10, "name": "Sarah P. Duke Gardens",        "lat": 36.0001, "lon": -78.9400, "type": "recreation"},
]

TYPE_COLORS = {
    "study":      "blue",
    "dining":     "orange",
    "recreation": "green",
    "academic":   "purple",
    "admin":      "gray",
    "parking":    "lightgray",
}

st.title("🗺️ Campus Map")
st.markdown("Browse Duke University buildings. Use the sidebar to filter by type or jump to a specific building.")

# ---------------------------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------------------------
all_types = sorted({b["type"] for b in BUILDINGS})
selected_types = st.sidebar.multiselect(
    "Filter by type",
    options=all_types,
    default=all_types,
    format_func=str.capitalize,
)

building_names = ["— none —"] + [b["name"] for b in BUILDINGS if b["type"] in selected_types]
selected_name = st.sidebar.selectbox("Jump to building", building_names)
selected_building = next((b for b in BUILDINGS if b["name"] == selected_name), None)

filtered = [b for b in BUILDINGS if b["type"] in selected_types]

# ---------------------------------------------------------------------------
# Build the Folium map
# ---------------------------------------------------------------------------
m = folium.Map(location=CAMPUS_CENTER, zoom_start=16, tiles="OpenStreetMap")
cluster = MarkerCluster().add_to(m)

for b in filtered:
    is_selected = selected_building and b["id"] == selected_building["id"]
    color = "red" if is_selected else TYPE_COLORS.get(b["type"], "blue")
    folium.Marker(
        location=[b["lat"], b["lon"]],
        popup=folium.Popup(f"<b>{b['name']}</b><br>Type: {b['type'].capitalize()}", max_width=200),
        tooltip=b["name"],
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(cluster)

# Zoom to selected building
if selected_building:
    m.location = [selected_building["lat"], selected_building["lon"]]
    m.zoom_start = 18

# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
st_folium(m, width="100%", height=520)

if selected_building:
    st.success(f"📍 **{selected_building['name']}** — {selected_building['type'].capitalize()}")
else:
    st.info("Select a building from the sidebar to highlight it on the map.")

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
st.markdown("**Map legend**")
cols = st.columns(len(TYPE_COLORS))
for col, (btype, color) in zip(cols, TYPE_COLORS.items()):
    col.markdown(f"🔵 {btype.capitalize()}" if color == "blue" else
                 f"🟠 {btype.capitalize()}" if color == "orange" else
                 f"🟢 {btype.capitalize()}" if color == "green" else
                 f"🟣 {btype.capitalize()}" if color == "purple" else
                 f"⚫ {btype.capitalize()}")
