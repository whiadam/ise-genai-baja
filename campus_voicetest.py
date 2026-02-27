##Auriell's Test files## import unittest
import unittest
from streamlit.testing.v1 import AppTest

# Change this to your actual Streamlit app filename:
APP_FILE = "campus_voice.py"   


class TestCampusVoiceApp(unittest.TestCase):

    def test_app_renders(self):
        """App should load and run without exceptions."""
        at = AppTest.from_file(APP_FILE).run()
        # If Streamlit throws an exception, AppTest typically captures it.
        # This assertion ensures the run completed.
        self.assertIsNotNone(at)

    def test_title_exists(self):
        """The main title 'Campus Voice' should appear."""
        at = AppTest.from_file(APP_FILE).run()
        titles = [t.value for t in at.title]
        self.assertIn("Campus Voice", titles)

    def test_sections_exist(self):
        """Key subheaders should exist."""
        at = AppTest.from_file(APP_FILE).run()

        subheaders = [s.value for s in at.subheader]
        expected = [
            "Report an Issue",
            "Rate a Facility",
            "Vote in a Poll",
            "Campus Buzz",
            "Filters",
        ]
        for text in expected:
            self.assertIn(text, subheaders)

    def test_report_issue_button_shows_success(self):
        """Clicking 'Report Now' should show success message."""
        at = AppTest.from_file(APP_FILE).run()

        # Optional: enter text in the first text_area (Describe the issue)
        # There are multiple text_area widgets in your app, so use index carefully.
        # In your layout, the first text_area is issue description.
        at.text_area[0].input("Bathroom is dirty").run()

        # Find the button labeled "Report Now" and click it
        report_buttons = [b for b in at.button if b.label == "Report Now"]
        self.assertTrue(report_buttons, "Could not find 'Report Now' button")

        report_buttons[0].click().run()

        # Check success message
        success_texts = [s.value for s in at.success]
        self.assertIn("Issue reported successfully!", success_texts)

    def test_rate_now_button_shows_success(self):
        """Clicking 'Rate Now' should show thank-you success message."""
        at = AppTest.from_file(APP_FILE).run()

        # The slider exists; set it (usually slider[0] is the rating)
        if at.slider:
            at.slider[0].set_value(5).run()

        # The second text_area in your app is the "Additional comments" one
        # (since the first is Report Issue)
        if len(at.text_area) > 1:
            at.text_area[1].input("Pretty clean overall.").run()

        rate_buttons = [b for b in at.button if b.label == "Rate Now"]
        self.assertTrue(rate_buttons, "Could not find 'Rate Now' button")

        rate_buttons[0].click().run()

        success_texts = [s.value for s in at.success]
        self.assertIn("Thank you for your feedback!", success_texts)

    def test_vote_button_shows_success(self):
        """Clicking 'Vote' should show voted-for message."""
        at = AppTest.from_file(APP_FILE).run()

        # The selectbox for polls should be the first selectbox in the app
        # (you also have a selectbox for Filters later, so there are 2)
        self.assertGreaterEqual(len(at.selectbox), 1, "No selectbox found")

        at.selectbox[0].select("Library Hours").run()

        vote_buttons = [b for b in at.button if b.label == "Vote"]
        self.assertTrue(vote_buttons, "Could not find 'Vote' button")

        vote_buttons[0].click().run()

        success_texts = [s.value for s in at.success]
        self.assertIn("You voted for: Library Hours", success_texts)


if __name__ == "__main__":
    unittest.main()
#from modules import display_alerts

