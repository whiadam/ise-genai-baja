# campus_map.py

import streamlit as st

def load_buildings():
    return [
        {"name": "Library", "lat": 33.881, "lon": -117.885},
        {"name": "Student Union", "lat": 33.882, "lon": -117.883},
        {"name": "Engineering Building", "lat": 33.883, "lon": -117.884},
    ]


def main():
    st.title("Campus Map")

    buildings = load_buildings()

    building_names = [b["name"] for b in buildings]

    selected = st.selectbox("Select a building", building_names)

    st.write(f"You selected: {selected}")


if __name__ == "__main__":
    main()
