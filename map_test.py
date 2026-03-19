# map_test.py
from streamlit.testing.v1 import AppTest


def test_app_renders_title_and_sidebar():
    at = AppTest.from_file("campus_map.py").run()
    assert at.title[0].value == "🏛️ Campus Map"
    assert at.sidebar.selectbox[0].value == "None"
    assert "Select Building:" in at.sidebar.selectbox[0].label


def test_building_selection_message():
    at = AppTest.from_file("campus_map.py").run()
    at.sidebar.selectbox[0].select("Library")
    at = at.run()
    assert "Selected: Library (study)" in at.success[0].value
