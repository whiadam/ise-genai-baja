#############################################################################
# campus_map.py
#
# Interactive campus map using Folium + streamlit-folium.
# Buildings are defined here as static data; swap in a BigQuery fetch
# (similar to get_active_polls in data_fetcher.py) whenever the DB table
# is ready.
#
# Coordinates verified against OpenStreetMap / Duke official map (maps.duke.edu)
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
# Coordinates verified via OpenStreetMap / maps.duke.edu
# ---------------------------------------------------------------------------
BUILDINGS = [
    # --- Academic / Study ---
    {"id": 1,  "name": "Perkins & Bostock Libraries",   "lat": 36.0022,  "lon": -78.9388,  "type": "study",
     "desc": "Main research libraries on West Campus"},
    {"id": 4,  "name": "Fitzpatrick Center (CIEMAS)",   "lat": 36.0020,  "lon": -78.9433,  "type": "academic",
     "desc": "Engineering and applied sciences building"},
    {"id": 6,  "name": "Allen Building (Admin)",         "lat": 36.0008,  "lon": -78.9374,  "type": "admin",
     "desc": "Duke University central administration"},
    {"id": 11, "name": "French Science Center",          "lat": 36.0030,  "lon": -78.9394,  "type": "academic",
     "desc": "Sciences and math building"},
    {"id": 12, "name": "Gross Hall",                     "lat": 36.0012,  "lon": -78.9449,  "type": "academic",
     "desc": "Energy & Environment / Data Science"},
    {"id": 13, "name": "Social Sciences Building",       "lat": 36.0011,  "lon": -78.9365,  "type": "academic",
     "desc": "Social sciences and humanities"},

    # --- Dining / Student Life ---
    {"id": 2,  "name": "Bryan Center",                   "lat": 36.0012,  "lon": -78.9411,  "type": "dining",
     "desc": "Student union, dining, and services"},
    {"id": 14, "name": "The Marketplace (East Campus)",  "lat": 36.0065,  "lon": -78.9225,  "type": "dining",
     "desc": "Main dining hall on East Campus"},

    # --- Recreation ---
    {"id": 3,  "name": "Wilson Recreation Center",       "lat": 36.0006,  "lon": -78.9444,  "type": "recreation",
     "desc": "Fitness center and recreational facilities"},
    {"id": 8,  "name": "Cameron Indoor Stadium",         "lat": 35.9947,  "lon": -78.9414,  "type": "recreation",
     "desc": "Home of Duke Blue Devils basketball"},
    {"id": 10, "name": "Sarah P. Duke Gardens",          "lat": 36.0003,  "lon": -78.9348,  "type": "recreation",
     "desc": "55-acre botanical garden on East-West border"},
    {"id": 15, "name": "Duke University Golf Club",      "lat": 36.0076,  "lon": -78.9513,  "type": "recreation",
     "desc": "18-hole golf course on Duke's West Campus"},
    {"id": 16, "name": "Karsh Alumni & Visitors Center", "lat": 36.0026,  "lon": -78.9463,  "type": "recreation",
     "desc": "Visitor information and alumni hub"},

    # --- Landmarks / Chapel ---
    {"id": 5,  "name": "Duke Chapel",                    "lat": 36.0024,  "lon": -78.9402,  "type": "landmark",
     "desc": "Iconic Gothic chapel at the heart of West Campus"},
    {"id": 9,  "name": "Nasher Museum of Art",           "lat": 36.0017,  "lon": -78.9367,  "type": "landmark",
     "desc": "Duke's fine arts museum with rotating exhibitions"},
    {"id": 17, "name": "Duke University Chapel Courtyard","lat": 36.0022, "lon": -78.9400,  "type": "landmark",
     "desc": "Central quad in front of Duke Chapel"},

    # --- Parking ---
    {"id": 7,  "name": "Bryan Center Parking Garage",    "lat": 36.0009,  "lon": -78.9422,  "type": "parking",
     "desc": "Main parking structure near Bryan Center"},
]

TYPE_COLORS = {
    "study":      "blue",
    "dining":     "orange",
    "recreation": "green",
    "academic":   "purple",
    "admin":      "gray",
    "parking":    "lightgray",
    "landmark":   "red",
}

TYPE_ICONS = {
    "study":      "book",
    "dining":     "cutlery",
    "recreation": "leaf",
    "academic":   "graduation-cap",
    "admin":      "cog",
    "parking":    "car",
    "landmark":   "star",
}

st.title("🗺️ Duke Campus Map")
st.markdown("Browse Duke University buildings and landmarks. Use the sidebar to filter by type or jump to a specific location.")

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
selected_name = st.sidebar.selectbox("Jump to location", building_names)
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
    icon  = TYPE_ICONS.get(b["type"], "info-sign")
    popup_html = f"<b>{b['name']}</b><br><i>{b['type'].capitalize()}</i><br>{b.get('desc', '')}"
    folium.Marker(
        location=[b["lat"], b["lon"]],
        popup=folium.Popup(popup_html, max_width=220),
        tooltip=b["name"],
        icon=folium.Icon(color=color, icon=icon, prefix="fa"),
    ).add_to(cluster)

# Zoom to selected building
if selected_building:
    m.location = [selected_building["lat"], selected_building["lon"]]
    m.zoom_start = 18

# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
st_folium(m, width="100%", height=540)

if selected_building:
    st.success(f"📍 **{selected_building['name']}** — {selected_building['type'].capitalize()} | {selected_building.get('desc', '')}")
else:
    st.info("Select a location from the sidebar to highlight it on the map.")

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
st.markdown("**Map legend**")
emoji_map = {
    "blue": "🔵", "orange": "🟠", "green": "🟢",
    "purple": "🟣", "gray": "⚫", "lightgray": "⚪", "red": "🔴",
}
cols = st.columns(len(TYPE_COLORS))
for col, (btype, color) in zip(cols, TYPE_COLORS.items()):
    col.markdown(f"{emoji_map.get(color, '📍')} {btype.capitalize()}")
