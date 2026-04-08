###AI WROTE THESE TESTS#######
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

with patch("google.cloud.bigquery.Client"):
    with patch("flyer_updater.agents.agent_service.query_agent", return_value="mocked response"):
        with patch("flyer_updater.agents.agent_service.get_or_create_session", return_value="mock-session"):
            from streamlit.testing.v1 import AppTest
            from flyer_updater.flyer import Flyer
            from flyer_updater import flyer_fetcher


class TestFlyerUpdater(unittest.TestCase):
    def setUp(self):
        self.at = AppTest.from_function(self._render_page)
        self.at.run()

    @staticmethod
    def _render_page():
        from flyer_updater.flyer_view import display_flyer_updater_page
        display_flyer_updater_page()

    def test_page_renders(self):
        self.assertFalse(self.at.exception)

    def test_header_displayed(self):
        self.assertEqual(self.at.header[0].value, "Event Creation Assistant")

    def test_radio_has_three_tabs(self):
        radio = self.at.radio[0]
        self.assertEqual(len(radio.options), 3)
        self.assertIn("Chat", radio.options)
        self.assertIn("Camera", radio.options)
        self.assertIn("Upload", radio.options)

    def test_default_tab_is_chat(self):
        self.assertEqual(self.at.radio[0].value, "Chat")

    def test_chat_input_exists(self):
        self.assertTrue(len(self.at.chat_input) > 0)

    def test_file_uploader_not_visible_on_chat_tab(self):
        self.assertEqual(len(self.at.file_uploader), 0)

    def test_camera_tab_renders_without_exception(self):
        self.at.radio[0].set_value("Camera").run()
        self.assertFalse(self.at.exception)

    def test_upload_tab_renders_without_exception(self):
        self.at.radio[0].set_value("Upload").run()
        self.assertFalse(self.at.exception)

    def test_file_uploader_visible_on_upload_tab(self):
        self.at.radio[0].set_value("Upload").run()
        self.assertEqual(len(self.at.file_uploader), 1)

###########################################################
## Test Flyer Fetcher
## had AI write these tests as well trying to prevent tendonitis
###########################################################


class TestFlyerFetcher(unittest.TestCase):

    @patch("flyer_updater.flyer_fetcher.run_query")
    def test_get_flyers(self, mock_run_query):
        mock_run_query.return_value = [
            {"flyer_id": 1, "upload_time": datetime(2026, 3, 23),
             "confidence_scores": None, "require_user_input": False,
             "fields_edited": [], "event_id": 42}
        ]
        result = flyer_fetcher.get_flyers()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].flyer_id, 1)
        self.assertEqual(result[0].event_id, 42)
        self.assertFalse(result[0].require_user_input)
        mock_run_query.assert_called_once()

    @patch("flyer_updater.flyer_fetcher.run_query")
    def test_get_flyers_empty(self, mock_run_query):
        mock_run_query.return_value = []
        result = flyer_fetcher.get_flyers()
        self.assertEqual(len(result), 0)

    @patch("flyer_updater.flyer_fetcher.run_query")
    def test_get_flyers_multiple(self, mock_run_query):
        mock_run_query.return_value = [
            {"flyer_id": 1, "upload_time": datetime(2026, 3, 23),
             "confidence_scores": None, "require_user_input": False,
             "fields_edited": [], "event_id": 42},
            {"flyer_id": 2, "upload_time": datetime(2026, 3, 24),
             "confidence_scores": None, "require_user_input": True,
             "fields_edited": ["event_title"], "event_id": 43}
        ]
        result = flyer_fetcher.get_flyers()
        self.assertEqual(len(result), 2)
        self.assertTrue(result[1].require_user_input)
        self.assertEqual(result[1].fields_edited, ["event_title"])

    @patch("flyer_updater.flyer_fetcher.get_client")
    def test_create_flyer(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.insert_rows_json.return_value = []
        mock_get_client.return_value = mock_client

        flyer = Flyer(
            flyer_id=1,
            upload_time=datetime(2026, 3, 23),
            confidence_scores={"event_title": 85, "event_location": 62},
            require_user_input=False,
            fields_edited=[],
            event_id=42,
        )
        result = flyer_fetcher.create_flyer(flyer)
        self.assertEqual(result, 1)
        mock_client.insert_rows_json.assert_called_once()

    @patch("flyer_updater.flyer_fetcher.get_client")
    def test_create_flyer_no_confidence_scores(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.insert_rows_json.return_value = []
        mock_get_client.return_value = mock_client

        flyer = Flyer(
            flyer_id=2,
            upload_time=datetime(2026, 3, 23),
        )
        result = flyer_fetcher.create_flyer(flyer)
        self.assertEqual(result, 2)
        mock_client.insert_rows_json.assert_called_once()

    @patch("flyer_updater.flyer_fetcher.get_client")
    def test_create_flyer_fails(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.insert_rows_json.return_value = [{"error": "something broke"}]
        mock_get_client.return_value = mock_client

        flyer = Flyer(
            flyer_id=1,
            upload_time=datetime(2026, 3, 23),
        )
        with self.assertRaises(Exception):
            flyer_fetcher.create_flyer(flyer)


if __name__ == "__main__":
    unittest.main()
