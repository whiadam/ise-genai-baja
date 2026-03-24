# event_module/event_fetcher_test.py
# Had AI write these tests in order to prevent carpal tunnel
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from event_module.event import Event

with patch("google.cloud.bigquery.Client"):
    from event_module import event_fetcher


class TestEventFetcher(unittest.TestCase):

    @patch("event_module.event_fetcher.run_query")
    def test_get_events(self, mock_run_query):
        mock_run_query.return_value = [
            {"event_id": 1, "time_created": datetime(2026, 3, 23), "event_startime": None,
             "event_endtime": None, "event_title": "Spring Concert", "event_location": "Main Hall",
             "department": "Music", "description": "Live music", "creator": "user1"}
        ]
        result = event_fetcher.get_events()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].event_title, "Spring Concert")
        self.assertEqual(result[0].department, "Music")
        mock_run_query.assert_called_once()

    @patch("event_module.event_fetcher.run_query")
    def test_get_events_empty(self, mock_run_query):
        mock_run_query.return_value = []
        result = event_fetcher.get_events()
        self.assertEqual(len(result), 0)

    @patch("event_module.event_fetcher.run_query")
    def test_get_upcoming_events(self, mock_run_query):
        mock_run_query.return_value = [
            {"event_id": 2, "time_created": datetime(2026, 3, 23), "event_startime": datetime(2026, 4, 1),
             "event_endtime": datetime(2026, 4, 1), "event_title": "Career Fair", "event_location": "Gym",
             "department": "CS", "description": "Networking event", "creator": "user2"}
        ]
        result = event_fetcher.get_upcoming_events()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].event_title, "Career Fair")
        mock_run_query.assert_called_once()

    @patch("event_module.event_fetcher.run_query")
    def test_get_upcoming_events_empty(self, mock_run_query):
        mock_run_query.return_value = []
        result = event_fetcher.get_upcoming_events()
        self.assertEqual(len(result), 0)

    @patch("event_module.event_fetcher.run_query")
    def test_get_events_by_department(self, mock_run_query):
        mock_run_query.return_value = [
            {"event_id": 3, "time_created": datetime(2026, 3, 23), "event_startime": None,
             "event_endtime": None, "event_title": "Hackathon", "event_location": "Lab",
             "department": "CS", "description": "Build stuff", "creator": "user3"}
        ]
        result = event_fetcher.get_events_by_department("CS")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].department, "CS")
        self.assertEqual(result[0].event_title, "Hackathon")

    @patch("event_module.event_fetcher.run_query")
    def test_get_events_by_department_wrong_department(self, mock_run_query):
        mock_run_query.return_value = []
        result = event_fetcher.get_events_by_department("Nonexistent")
        self.assertEqual(len(result), 0)

    @patch("event_module.event_fetcher.get_client")
    def test_create_event(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.insert_rows_json.return_value = []
        mock_get_client.return_value = mock_client

        event = Event(
            event_id=1,
            time_created=datetime(2026, 3, 23),
            creator="user1",
            event_title="Test Event",
            event_location="Room 101",
            department="CS",
            description="A test",
        )
        result = event_fetcher.create_event(event)
        self.assertEqual(result, 1)
        mock_client.insert_rows_json.assert_called_once()

    @patch("event_module.event_fetcher.get_client")
    def test_create_event_fails(self, mock_get_client):
        mock_client = MagicMock()
        mock_client.insert_rows_json.return_value = [{"error": "something broke"}]
        mock_get_client.return_value = mock_client

        event = Event(
            event_id=1,
            time_created=datetime(2026, 3, 23),
            creator="user1",
        )
        with self.assertRaises(Exception):
            event_fetcher.create_event(event)


if __name__ == "__main__":
    unittest.main()  unittest.main()
