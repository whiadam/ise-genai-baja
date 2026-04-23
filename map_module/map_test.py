# map_module/map_fetcher_test.py
import unittest
from unittest.mock import patch, MagicMock

with patch("config.get_client", return_value=MagicMock()):
    from map_module import map_fetcher


class TestMapFetcher(unittest.TestCase):

    @patch("config.get_client", return_value=MagicMock())
    @patch("map_module.map_fetcher.run_query")          # ← fixed
    def test_get_user_profile(self, mock_run_query, _mock_client):
        mock_row = MagicMock()
        mock_row.full_name = "John Doe"
        mock_row.username = "johndoe"
        mock_row.date_of_birth = "2000-01-01"
        mock_row.profile_image = "profile.jpg"
        mock_row.friends = ["friend1", "friend2"]
        mock_run_query.return_value = [mock_row]

        result = map_fetcher.get_user_profile("user123")

        self.assertEqual(result["full_name"], "John Doe")
        self.assertEqual(result["username"], "johndoe")
        self.assertEqual(result["friends"], ["friend1", "friend2"])

    @patch("config.get_client", return_value=MagicMock())
    @patch("map_module.map_fetcher.run_query")          # ← fixed
    def test_get_user_profile_not_found(self, mock_run_query, _mock_client):
        mock_run_query.return_value = []

        result = map_fetcher.get_user_profile("nonexistent")

        self.assertIsNone(result)

    @patch("config.get_client", return_value=MagicMock())
    @patch("map_module.map_fetcher.run_query")          # ← fixed
    def test_get_user_posts(self, mock_run_query, _mock_client):
        mock_row = MagicMock()
        mock_row.user_id = "user123"
        mock_row.post_id = "post1"
        mock_row.timestamp = "2026-03-29 10:00:00"
        mock_row.content = "Event at library!"
        mock_row.image = None
        mock_run_query.return_value = [mock_row]

        result = map_fetcher.get_user_posts("user123")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["post_id"], "post1")
        self.assertIsNone(result[0]["image"])

    @patch("config.get_client", return_value=MagicMock())
    @patch("map_module.map_fetcher._get_genai_model")   # ← fixed
    @patch("map_module.map_fetcher.get_user_profile")   # ← fixed
    def test_get_genai_advice(self, mock_profile, mock_model, _mock_client):
        mock_profile.return_value = {
            "full_name": "John Doe",
            "username": "johndoe",
            "date_of_birth": "2000-01-01",
            "profile_image": None,
            "friends": [],
        }
        mock_response = MagicMock()
        mock_response.text = "Check out the events on campus this week!"
        mock_model.return_value.generate_content.return_value = mock_response

        result = map_fetcher.get_genai_advice("user123")

        self.assertEqual(result["advice_id"], "genai-advice-1")
        self.assertIsNone(result["image"])
        self.assertIn("content", result)

    @patch("config.get_client", return_value=MagicMock())
    @patch("map_module.map_fetcher.get_user_profile")   # ← fixed
    def test_get_genai_advice_no_profile(self, mock_profile, _mock_client):
        mock_profile.return_value = None

        result = map_fetcher.get_genai_advice("ghost_user")

        self.assertIsNone(result["image"])
        self.assertTrue(len(result["content"]) > 0)


if __name__ == "__main__":
    unittest.main()