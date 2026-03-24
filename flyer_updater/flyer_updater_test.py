import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

VIEW_PATH = str(Path(__file__).parent / "view.py")

class TestFlyerUpdater(unittest.TestCase):

    def setUp(self):
       self.at = AppTest.from_function(self._render_page)
       self.at.run()
    
    @staticmethod
    def _render_page():
        from flyer_updater.flyer_view import display_flyer_updater_page
        display_flyer_updater_page()

    def test_page_renders(self):
        self.assertFalse(self.at.exception)

    def test_title_displayed(self):
        self.assertEqual(self.at.title[0].value, "Flyer Updater")

    def test_submit_without_image_shows_warning(self):
        self.at.button[0].click().run()
        self.assertEqual(len(self.at.warning), 1)

