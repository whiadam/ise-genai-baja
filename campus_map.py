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
# CSUF campus center  (33.8823° N, 117.8851° W)
# ---------------------------------------------------------------------------
CAMPUS_CENTER = [33.8823, -117.8851]

# ---------------------------------------------------------------------------
# Building data — replace / extend with a BigQuery fetch when ready
# ---------------------------------------------------------------------------
BUILDINGS = [
    {"id": 1,  "name": "Pollak Library",            "lat": 33.8824, "lon": -117.8849, "type": "study"},
    {"id": 2,  "name": "Titan Student Union",        "lat": 33.8830, "lon": -117.8862, "type": "dining"},
    {"id": 3,  "name": "Student Recreation Center", "lat": 33.8817, "lon": -117.8878, "type": "recreation"},
    {"id": 4,  "name": "CS & Engineering Building", "lat": 33.8820, "lon": -117.8835, "type": "academic"},
    {"id": 5,  "name": "McCarthy Hall",              "lat": 33.8810, "lon": -117.8851, "type": "academic"},
    {"id": 6,  "name": "University Hall",            "lat": 33.8832, "lon": -117.8844, "type": "admin"},
    {"id": 7,  "name": "Nutwood Parking Structure", "lat": 33.8798, "lon": -117.8855, "type": "parking"},
    {"id": 8,  "name": "Titan Gymnasium",            "lat": 33.8840, "lon": -117.8870, "type": "recreation"},
    {"id": 9,  "name": "Visual Arts Building",       "lat": 33.8806, "lon": -117.8838, "type": "academic"},
    {"id": 10, "name": "Langsdorf Hall",             "lat": 33.8837, "lon": -117.8853, "type": "admin"},
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
st.markdown("Browse CSUF buildings. Use the sidebar to filter by type or jump to a specific building.")

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
