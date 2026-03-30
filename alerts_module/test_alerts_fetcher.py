########################### Imports ############################
import unittest
from unittest.mock import MagicMock, patch

import alerts_fetcher

################### Danae's Tests #########################
class TestAlertDataFetcher(unittest.TestCase):
    """
    Test suite for alert-related BigQuery and GenAI data fetcher functions.
    """

    @patch("alerts_fetcher.get_bigquery_client")
    def test_get_all_alerts_returns_all_rows(self, mock_get_bigquery_client):
        """
        All lines in this function written by GPT-5.2 Thinking

        Verifies get_all_alerts returns all rows from the database as dictionaries.
        """
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [
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
        mock_client.query.return_value = mock_query_job
        mock_get_bigquery_client.return_value = mock_client

        result = alerts_fetcher.get_all_alerts()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["alert_id"], 1)
        mock_client.query.assert_called_once()

    @patch("alerts_fetcher.get_bigquery_client")
    def test_get_alert_by_id_returns_matching_alert(self, mock_get_bigquery_client):
        """
        All lines in this function written by GPT-5.2 Thinking
        """
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [
            {"alert_id": 5, "alert_name": "Advisor Meeting"}
        ]
        mock_client.query.return_value = mock_query_job
        mock_get_bigquery_client.return_value = mock_client

        result = alerts_fetcher.get_alert_by_id(5)

        self.assertIsNotNone(result)
        self.assertEqual(result["alert_id"], 5)

    @patch("alerts_fetcher.get_bigquery_client")
    def test_get_alert_by_id_returns_none(self, mock_get_bigquery_client):
        """
        All lines in this function written by GPT-5.2 Thinking
        """
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []
        mock_client.query.return_value = mock_query_job
        mock_get_bigquery_client.return_value = mock_client

        result = alerts_fetcher.get_alert_by_id(999)

        self.assertIsNone(result)

    @patch("alerts_fetcher.get_bigquery_client")
    def test_get_alerts_by_preference(self, mock_get_bigquery_client):
        """
        All lines in this function written by GPT-5.2 Thinking
        """
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [
            {"alert_id": 7, "preference": ["Email", "Text"]}
        ]
        mock_client.query.return_value = mock_query_job
        mock_get_bigquery_client.return_value = mock_client

        result = alerts_fetcher.get_alerts_by_preference("Email")

        self.assertEqual(len(result), 1)
        self.assertIn("Email", result[0]["preference"])

    @patch("alerts_fetcher.get_bigquery_client")
    def test_get_recurring_alerts(self, mock_get_bigquery_client):
        """
        All lines in this function written by GPT-5.2 Thinking
        """
        mock_client = MagicMock()
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [
            {"alert_id": 11, "reoccuring": True}
        ]
        mock_client.query.return_value = mock_query_job
        mock_get_bigquery_client.return_value = mock_client

        result = alerts_fetcher.get_recurring_alerts()

        self.assertTrue(all(a["reoccuring"] for a in result))

    @patch("alerts_fetcher.GenerativeModel")
    @patch("alerts_fetcher.vertexai.init")
    @patch("alerts_fetcher.get_all_alerts")
    def test_get_genai_alert_summary(
        self,
        mock_get_all_alerts,
        mock_vertexai_init,
        mock_generative_model,
    ):
        """
        All lines in this function written by GPT-5.2 Thinking
        """
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