import unittest
from unittest.mock import patch, MagicMock
import data_fetcher


class TestDataFetcher(unittest.TestCase):

    @patch("data_fetcher.client")
    def test_get_user_posts(self, mock_client):
        # Fake row returned from BigQuery
        mock_row = MagicMock(
            IssueId="issue1",
            UserId="user1",
            IssueText="Bathroom is dirty",
            CreatedAt="2026-03-23 09:00:00",
        )

        mock_client.query.return_value.result.return_value = [mock_row]

        result = data_fetcher.get_user_posts("user1")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user_id"], "user1")
        self.assertEqual(result[0]["content"], "Bathroom is dirty")


    @patch("data_fetcher.client")
    def test_get_active_polls(self, mock_client):
        mock_row = MagicMock(
            PollId="poll1",
            PollQuestion="What food should the dining hall have more often?",
            CreatedAt="2026-03-23 10:00:00",
            Category="Food",
            IsActive=True,
        )

        mock_client.query.return_value.result.return_value = [mock_row]

        result = data_fetcher.get_active_polls()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["poll_id"], "poll1")
        self.assertTrue(result[0]["is_active"])


    @patch("data_fetcher.client")
    def test_get_filtered_issues(self, mock_client):
        mock_row = MagicMock(
            IssueId="issue1",
            UserId="user1",
            IssueText="Bathroom is dirty",
            Category="Cleanliness",
            CreatedAt="2026-03-23 09:00:00",
            Status="Open",
        )

        mock_client.query.return_value.result.return_value = [mock_row]

        result = data_fetcher.get_filtered_issues("Cleanliness")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["category"], "Cleanliness")
        self.assertEqual(result[0]["status"], "Open")


    @patch("data_fetcher.client")
    def test_get_user_profile_no_data(self, mock_client):
        # Simulate no rows
        mock_client.query.return_value.result.return_value = []

        result = data_fetcher.get_user_profile("user1")

        self.assertEqual(result["username"], "student")
        self.assertEqual(result["full_name"], "Campus User")


    @patch("data_fetcher.get_active_polls")
    @patch("data_fetcher.get_filtered_issues")
    def test_get_genai_data(self, mock_get_filtered_issues, mock_get_active_polls):
        # Fake data for genAI logic
        mock_get_filtered_issues.return_value = [{"issue_id": "issue1"}]
        mock_get_active_polls.return_value = [{"poll_id": "poll1"}]

        result = data_fetcher.get_genai_data("user1")

        self.assertIn("content", result)
        self.assertEqual(result["advice_id"], "genai1")
        self.assertIsNone(result["image"])


if __name__ == "__main__":
    unittest.main()