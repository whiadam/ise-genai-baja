#############################################################################
# TESTS FOR FLYER_UPDATER MODULE#############################################

import unittest
from streamlit.testing.v1 import AppTest
#from modules import display_alerts
class TestFlyerUpdater(unittest.TestCase):

    def test_page_renders(self):
        at = AppTest.from_file("flyer_updater/view.py")
        at.run()
        self.assertFalse(at.exception)

    def test_title_displayed(self):
        at = AppTest.from_file("flyer_updater/view.py")
        at.run()
        self.assertEqual(at.title[0].value, "Flyer Updater")

    def test_submit_without_image_shows_warning(self):
        at = AppTest.from_file("flyer_updater/view.py")
        at.run()
        at.button[0].click().run()
        self.assertEqual(len(at.warning), 1)

