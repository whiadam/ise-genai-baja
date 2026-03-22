########################### Imports ############################
import unittest
from datetime import datetime, timedelta
from streamlit.testing.v1 import AppTest

################### Danae's Tests #########################
class TestAlertsModule(unittest.TestCase):
    """
    Test suite for the Alerts module using Streamlit AppTest.
    """

    def _make_test_app(self) -> str:
        """
        Returns a minimal Streamlit app as a string that renders display_alerts().
        """
        return """
import streamlit as st
from datetime import datetime, timedelta
from modules import display_alerts

events = [{"name": "Test Event", "start": datetime.now().replace(second=0, microsecond=0) + timedelta(hours=2)}]

display_alerts(user_id="user1", events=events)
"""

    def test_create_alert_adds_to_list(self):
        """
        Creates an alert through the form and verifies it is stored.
        """
        at = AppTest.from_string(self._make_test_app())
        at.run()

        at.text_input("alerts_title_input").set_value("CS Club Meeting")
        at.selectbox("alerts_category_select").set_value("Academic")
        at.selectbox("alerts_type_select").set_value("Personal Reminder")

        at.button("FormSubmitter:create_alert_form-Save Alert").click()
        at.run()

        self.assertEqual(len(at.session_state["alerts"]), 1)
        alert = at.session_state["alerts"][0]
        self.assertEqual(alert["title"], "CS Club Meeting")
        self.assertEqual(alert["category"], "Academic")
        self.assertEqual(alert["alert_type"], "Personal Reminder")
        self.assertTrue(alert["enabled"])


    def test_disable_alert_marks_disabled(self):
        """
        Adds an alert directly to session_state then clicks Disable.
        """
        at = AppTest.from_string(self._make_test_app())
        at.run()

        at.session_state["alerts"] = [
            {
                "id": 1,
                "user_id": "user1",
                "title": "Injected Alert",
                "category": "Other",
                "alert_type": "Campus Announcement",
                "minutes_before": None,
                "event_start": None,
                "event_name": None,
                "remind_at": None,
                "delivery": {"in_app": True, "email": False, "sms": False},
                "enabled": True,
                "created_at": datetime.now(),
            }
        ]

        at.run()
        at.button("disable_1").click()
        at.run()

        self.assertFalse(at.session_state["alerts"][0]["enabled"])


    def test_delete_alert_removes_it(self):
        """
        Adds an alert directly then clicks Delete and verifies it is removed.
        """
        at = AppTest.from_string(self._make_test_app())
        at.run()

        at.session_state["alerts"] = [
            {
                "id": 1,
                "user_id": "user1",
                "title": "Delete Me",
                "category": "Other",
                "alert_type": "Campus Announcement",
                "minutes_before": None,
                "event_start": None,
                "event_name": None,
                "remind_at": None,
                "delivery": {"in_app": True, "email": False, "sms": False},
                "enabled": True,
                "created_at": datetime.now(),
            }
        ]

        at.run()
        at.button("delete_1").click()
        at.run()

        self.assertEqual(at.session_state["alerts"], [])

#################### End of Danae's Tests #########################


if __name__ == "__main__":
    unittest.main()
