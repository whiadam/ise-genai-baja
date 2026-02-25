#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from datetime import datetime, timedelta
from streamlit.testing.v1 import AppTest
#from modules import display_alerts

# Write your tests below

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

    def test_alerts_initializes_session_state(self):
        """
        Verifies display_alerts initializes expected session_state keys.
        """
        at = AppTest.from_string(self._make_test_app())
        at.run()

        self.assertIn("alerts", at.session_state)
        self.assertIsInstance(at.session_state["alerts"], list)
        self.assertIn("next_alert_id", at.session_state)
        self.assertIn("dismissed_banner_ids", at.session_state)

    def test_create_alert_adds_to_list(self):
        """
        Creates an alert through the form and verifies it is stored.
        """
        at = AppTest.from_string(self._make_test_app())
        at.run()

        at.text_input("Alert Title").set_value("CS Club Meeting")
        at.selectbox("Category").set_value("Academic")
        at.selectbox("Alert Type").set_value("Personal Reminder")

        at.form("create_alert_form").submit()
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
        at.button("Disable").click()
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
        at.button("Delete").click()
        at.run()

        self.assertEqual(at.session_state["alerts"], [])

    def test_upcoming_alerts_table_shows_future_alert(self):
        """
        Creates a future alert and checks that an Upcoming Alerts table is rendered.
        """
        at = AppTest.from_string(self._make_test_app())
        at.run()

        future_time = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=3)

        at.session_state["alerts"] = [
            {
                "id": 1,
                "user_id": "user1",
                "title": "Future Reminder",
                "category": "Academic",
                "alert_type": "Personal Reminder",
                "minutes_before": None,
                "event_start": None,
                "event_name": None,
                "remind_at": future_time,
                "delivery": {"in_app": True, "email": False, "sms": False},
                "enabled": True,
                "created_at": datetime.now(),
            }
        ]

        at.run()

        self.assertGreaterEqual(len(at.dataframe), 1)

#################### End of Danae's Tests #########################


if __name__ == "__main__":
    unittest.main()
