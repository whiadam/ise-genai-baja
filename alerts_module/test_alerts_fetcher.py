########################### Imports ############################
import unittest
from unittest.mock import MagicMock, patch

from alerts_module import alerts_fetcher

################### Danae's Tests #########################
class TestAlertDataFetcher(unittest.TestCase):
    """Test suite for alert-related BigQuery and GenAI data fetcher functions."""

    @patch("alerts_module.alerts_fetcher.run_query")
    def test_get_all_alerts_returns_all_rows(self, mock_run_query):
        """Verifies get_all_alerts returns all rows from the database as dictionaries."""
        mock_run_query.return_value = [
            {
                "alert_id": 1,
                "preference": ["Email", "Text"],
                "time_of_alert": "2026-04-01 10:00:00",
                "reoccuring": True,
                "alert_name": "Career Fair Alert",
                "alert_description": "Attend the career fair",
                "event_id": 101,
            }
        ]

        result = alerts_fetcher.get_all_alerts()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["alert_id"], 1)
        mock_run_query.assert_called_once()

    @patch("alerts_module.alerts_fetcher.run_query")
    def test_get_alert_by_id_returns_matching_alert(self, mock_run_query):
        mock_run_query.return_value = [
            {"alert_id": 5, "alert_name": "Advisor Meeting"}
        ]

        result = alerts_fetcher.get_alert_by_id(5)

        self.assertIsNotNone(result)
        self.assertEqual(result["alert_id"], 5)
        mock_run_query.assert_called_once()

    @patch("alerts_module.alerts_fetcher.run_query")
    def test_get_alert_by_id_returns_none(self, mock_run_query):
        mock_run_query.return_value = []

        result = alerts_fetcher.get_alert_by_id(999)

        self.assertIsNone(result)
        mock_run_query.assert_called_once()

    @patch("alerts_module.alerts_fetcher.run_query")
    def test_get_alerts_by_preference(self, mock_run_query):
        mock_run_query.return_value = [
            {"alert_id": 7, "preference": ["Email", "Text"]}
        ]

        result = alerts_fetcher.get_alerts_by_preference("Email")

        self.assertEqual(len(result), 1)
        self.assertIn("Email", result[0]["preference"])
        mock_run_query.assert_called_once()

    @patch("alerts_module.alerts_fetcher.run_query")
    def test_get_recurring_alerts(self, mock_run_query):
        mock_run_query.return_value = [
            {"alert_id": 11, "reoccuring": True},
            {"alert_id": 12, "reoccuring": True},
        ]

        result = alerts_fetcher.get_recurring_alerts()

        self.assertTrue(all(a["reoccuring"] for a in result))
        mock_run_query.assert_called_once()

    @patch("alerts_module.alerts_fetcher.GenerativeModel")
    @patch("alerts_module.alerts_fetcher.vertexai.init")
    @patch("alerts_module.alerts_fetcher.get_all_alerts")
    def test_get_genai_alert_summary(
        self,
        mock_get_all_alerts,
        mock_vertexai_init,
        mock_generative_model,
    ):
        mock_get_all_alerts.return_value = [
            {
                "alert_name": "Test Alert",
                "time_of_alert": "2026-04-01 10:00:00",
                "preference": ["Email", "Text"],
            }
        ]

        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Summary text"
        mock_generative_model.return_value = mock_model

        result = alerts_fetcher.get_genai_alert_summary()

        self.assertIsInstance(result, str)
        self.assertIn("Summary", result)


#################### End of Danae's Tests #########################

if __name__ == "__main__":
    unittest.main()
