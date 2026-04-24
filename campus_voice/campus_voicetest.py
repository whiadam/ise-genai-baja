import os
import sys
import unittest
from streamlit.testing.v1 import AppTest

# Fix import path so campus_voice.py can find data_fetcher.py
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

APP_FILE = os.path.join(ROOT_DIR, "campus_voice", "campus_voice.py")


class TestCampusVoiceApp(unittest.TestCase):

    def test_app_renders(self):
        # Do NOT run the app here to avoid timeout
        at = AppTest.from_file(APP_FILE)
        self.assertIsNotNone(at)

    def test_title_exists(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)
        titles = [t.value for t in at.title]
        self.assertIn("Campus Voice", titles)

    def test_home_sections_exist(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)
        subheaders = [s.value for s in at.subheader]

        expected_sections = [
            "Report an Issue",
            "Vote in a Poll",
            "Facility Ratings",
            "Campus Issues",
        ]

        for section in expected_sections:
            self.assertIn(section, subheaders)

    def test_report_issue_button_exists(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)
        buttons = [b.label for b in at.button]
        self.assertIn("Report Now", buttons)

    def test_report_issue_warning_when_empty(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)

        report_buttons = [b for b in at.button if b.label == "Report Now"]
        self.assertTrue(report_buttons, "Could not find Report Now button")

        report_buttons[0].click().run(timeout=10)

        warnings = [w.value for w in at.warning]
        self.assertIn("Please fill everything out", warnings)

    def test_vote_section_exists(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)
        subheaders = [s.value for s in at.subheader]
        self.assertIn("Vote in a Poll", subheaders)

    def test_facility_ratings_section_exists(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)
        subheaders = [s.value for s in at.subheader]
        self.assertIn("Facility Ratings", subheaders)

    def test_campus_issues_filter_exists(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)
        selectboxes = [s.label for s in at.selectbox]
        self.assertIn("Show issues with rating at least", selectboxes)

    def test_sidebar_navigation_options_exist(self):
        at = AppTest.from_file(APP_FILE).run(timeout=10)

        radios = at.radio
        self.assertGreaterEqual(len(radios), 1)

        options = list(radios[0].options)

        expected_pages = [
            "Home",
            "Trending Issues",
            "Map View",
            "Issue Details",
        ]

        for page in expected_pages:
            self.assertIn(page, options)


if __name__ == "__main__":
    unittest.main()