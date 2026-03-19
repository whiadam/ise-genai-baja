import pytest
from streamlit.testing.v1 import AppTest
import unittest




class TestCampusMapApp(unittest.TestCase):

# Checks the app loads with the right amount of buildings
    def test_map_loads_buildings(self):
        at = AppTest.from_file("map.py").run()
        assert at.sidebar.selectbox[0].value == "None"
        #assert len(at.map_markers) == 5  
        assert "Campus Map" in at.title[0].value

    # tests the building selection
    def test_building_selection(self):
        at = AppTest.from_file("map.py").run()
        at.sidebar.selectbox[0].select("Library")  
        at.run()
        assert at.success[0].value == "Selected: Library (study)"  


if __name__ == "__main__":
    unittest.main()
