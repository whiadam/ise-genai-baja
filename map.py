"""import streamlit as st
from modules import display_my_custom_component, display_alerts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
userId = 'user1'
def display_app_page():
    ""Displays the home page of the app.""
    st.title("Campus Map App")
# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
    THIS IS AN AI MOCKUP I TAKE NO CREDIT AND FOR SOME REASON I HAD TO DOWNLOAD STREAMLIT AS A COMMAND AGAIN
"""
###########################################################################
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Campus center (adjust coordinates to your campus)
campus_center = [33.7490, -84.3880]  # Example: Georgia Tech area

# Buildings data from your app
buildings = [
    {"id": 1, "name": "Student Union", "lat": 33.7495, "lon": -84.3875, "type": "dining"},
    {"id": 2, "name": "Library", "lat": 33.7500, "lon": -84.3860, "type": "study"},
    {"id": 3, "name": "Gym", "lat": 33.7480, "lon": -84.3855, "type": "recreation"},
    {"id": 4, "name": "Science Hall", "lat": 33.7475, "lon": -84.3870, "type": "academic"},
    {"id": 5, "name": "Dorms", "lat": 33.7505, "lon": -84.3885, "type": "housing"},
]

st.title("🏛️ Campus Map")
st.markdown("Click markers for details. Select a building below to highlight.")

# Sidebar for building selection
selected_id = st.sidebar.selectbox("Select Building:", ["None"] + [b["name"] for b in buildings])
selected_building = next((b for b in buildings if b["name"] == selected_id), None) if selected_id != "None" else None

# Create map
m = folium.Map(location=campus_center, zoom_start=16, tiles="OpenStreetMap")

# Add building markers
cluster = MarkerCluster().add_to(m)
for building in buildings:
    color = "orange" if building["id"] == (selected_building["id"] if selected_building else 0) else "blue"
    folium.Marker(
        [building["lat"], building["lon"]],
        popup=f"<b>{building['name']}</b><br>Type: {building['type']}",
        tooltip=building["name"],
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(cluster)

# Fit map to buildings
bounds = [[b["lat"] for b in buildings], [b["lon"] for b in buildings]]
m.fit_bounds([min(bounds[0]), min(bounds[1]), max(bounds[0]), max(bounds[1])])

folium_static(m)

if selected_building:
    st.success(f"Selected: {selected_building['name']} ({selected_building['type']})")
else:
    st.info("No building selected.")