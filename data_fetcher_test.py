import unittest
from unittest.mock import patch, MagicMock

with patch("google.cloud.bigquery.Client"):
    import data_fetcher

class TestDataFetcher(unittest.TestCase):

    @patch("config.run_query")
    def test_get_active_polls(self, mock_run_query):
        mock_row = MagicMock(
            PollId="poll1",
            PollQuestion="What food should the dining hall have more often?",
            CreatedAt="2026-03-23 10:00:00",
            Category="Food",
            IsActive=True,
        )
        mock_run_query.return_value = [mock_row]

        result = data_fetcher.get_active_polls()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["poll_id"], "poll1")
        self.assertTrue(result[0]["is_active"])

    @patch("config.run_query")
    def test_get_issues(self, mock_run_query):
        mock_row = MagicMock(
            issue_id="issue1",
            Title="Dirty Bathroom",
            Description="The bathroom is not clean.",
            Time_stamp="2026-03-23 10:00:00",
            Rating=2,
        )
        mock_run_query.return_value = [mock_row]

        result = data_fetcher.get_issues()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["issue_id"], "issue1")
        self.assertEqual(result[0]["title"], "Dirty Bathroom")
        self.assertEqual(result[0]["rating"], 2)

    @patch("config.run_query")
    def test_get_filtered_issues(self, mock_run_query):
        mock_row = MagicMock(
            issue_id="issue2",
            Title="Broken Vending Machine",
            Description="Machine is broken.",
            Time_stamp="2026-03-23 11:00:00",
            Rating=3,
        )
        mock_run_query.return_value = [mock_row]

        result = data_fetcher.get_filtered_issues(3)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["issue_id"], "issue2")
        self.assertEqual(result[0]["rating"], 3)

    @patch("config.run_query")
    def test_get_facility_ratings(self, mock_run_query):
        mock_row = MagicMock(
            RatingId="rating1",
            UserId="user1",
            FacilityName="Library",
            Rating=5,
            Comment="Very clean",
            CreatedAt="2026-03-23 11:00:00",
        )
        mock_run_query.return_value = [mock_row]

        result = data_fetcher.get_facility_ratings()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["facility_name"], "Library")
        self.assertEqual(result[0]["rating"], 5)

    @patch("data_fetcher._get_genai_model")
    @patch("data_fetcher.get_facility_ratings")
    @patch("data_fetcher.get_issues")
    @patch("data_fetcher.get_active_polls")
    def test_get_genai_data(
        self,
        mock_get_active_polls,
        mock_get_issues,
        mock_get_facility_ratings,
        mock_get_genai_model,
    ):
        mock_get_active_polls.return_value = [{"poll_id": "poll1"}]
        mock_get_issues.return_value = [{"issue_id": "issue1"}]
        mock_get_facility_ratings.return_value = [{"rating": 4}]

        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Campus Voice is active and students are engaged."
        mock_model.generate_content.return_value = mock_response
        mock_get_genai_model.return_value = mock_model

        result = data_fetcher.get_genai_data("user1")

        self.assertEqual(result["advice_id"], "genai1")
        self.assertIn("content", result)
        self.assertTrue(len(result["content"]) > 0)

# ─────────────────────────────────────────────────────────────────────────────
# Adams Added Tests:
# ─────────────────────────────────────────────────────────────────────────────
    @patch("config.run_query")
    def test_get_user_profile(self, mock_run_query):
        mock_row = MagicMock()
        mock_row.full_name = "John Doe"
        mock_row.username = "johndoe"
        mock_row.date_of_birth = "2000-01-01"
        mock_row.profile_image = "profile.jpg"
        mock_row.friends = ["friend1", "friend2"]
        mock_run_query.return_value = [mock_row]
        result = data_fetcher.get_user_profile("user123")
        self.assertEqual(result["full_name"], "John Doe")
        self.assertEqual(result["username"], "johndoe")
        self.assertEqual(result["friends"], ["friend1", "friend2"])

    @patch("config.run_query")
    def test_get_user_profile_not_found(self, mock_run_query):
        mock_run_query.return_value = []
        result = data_fetcher.get_user_profile("nonexistent")
        self.assertIsNone(result)

    @patch("config.run_query")
    def test_get_user_posts(self, mock_run_query):
        mock_row = MagicMock()
        mock_row.user_id = "user123"
        mock_row.post_id = "post1"
        mock_row.timestamp = "2026-03-29 10:00:00"
        mock_row.content = "Event at library!"
        mock_row.image = None
        mock_run_query.return_value = [mock_row]
        result = data_fetcher.get_user_posts("user123")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["post_id"], "post1")
        self.assertIsNone(result[0]["image"])

    @patch("data_fetcher._get_genai_model")
    @patch("data_fetcher.get_user_profile")
    def test_get_genai_advice(self, mock_profile, mock_model):
        mock_profile.return_value = {
            "full_name": "John Doe", "username": "johndoe",
            "date_of_birth": "2000-01-01", "profile_image": None, "friends": []
        }
        mock_response = MagicMock()
        mock_response.text = "Check out the events on campus this week!"
        mock_model.return_value.generate_content.return_value = mock_response
        result = data_fetcher.get_genai_advice("user123")
        self.assertEqual(result["advice_id"], "genai-advice-1")
        self.assertIsNone(result["image"])
        self.assertIn("content", result)

    @patch("data_fetcher.get_user_profile")
    def test_get_genai_advice_no_profile(self, mock_profile):
        mock_profile.return_value = None
        result = data_fetcher.get_genai_advice("ghost_user")
        self.assertIsNone(result["image"])
        self.assertTrue(len(result["content"]) > 0)

if __name__ == "__main__":
    unittest.main()
