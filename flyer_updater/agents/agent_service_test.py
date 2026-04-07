# ADDED WITH AI
import unittest
from unittest.mock import patch, MagicMock, AsyncMock

with patch("google.cloud.bigquery.Client"):
    from flyer_updater.agents import agent_service


class TestAgentService(unittest.TestCase):

    @patch("flyer_updater.agents.agent._get_runner_and_session")
    def test_query_agent_text_only(self, mock_get_runner_and_session):
        mock_runner = MagicMock()
        mock_get_runner_and_session.return_value = (mock_runner, MagicMock())

        mock_event = MagicMock()
        mock_event.is_final_response.return_value = True
        mock_event.content.parts = [MagicMock(text="Extracted event data")]

        async def fake_run(**_):
            yield mock_event

        mock_runner.run_async = fake_run

        result = str(agent_service.query_agent("user1", "session1", "extract this"))
        self.assertIn("Extracted", result)

    @patch("flyer_updater.agents.agent._get_runner_and_session")
    def test_query_agent_empty_response(self, mock_get_runner_and_session):
        mock_runner = MagicMock()
        mock_get_runner_and_session.return_value = (mock_runner, MagicMock())

        mock_event = MagicMock()
        mock_event.is_final_response.return_value = False
        mock_event.content = None

        async def fake_run(**_):
            yield mock_event

        mock_runner.run_async = fake_run

        result = agent_service.query_agent("user1", "session1", "hello")
        self.assertEqual(result, "")

    @patch("flyer_updater.agents.agent._get_runner_and_session")
    def test_query_agent_with_image(self, mock_get_runner_and_session):
        mock_runner = MagicMock()
        mock_get_runner_and_session.return_value = (mock_runner, MagicMock())

        mock_event = MagicMock()
        mock_event.is_final_response.return_value = True
        mock_event.content.parts = [MagicMock(text="Found: Spring Concert")]

        async def fake_run(**_):
            yield mock_event

        mock_runner.run_async = fake_run

        mock_image = MagicMock()
        mock_image.getvalue.return_value = b"fake_image_bytes"
        mock_image.type = "image/png"

        result = str(agent_service.query_agent("user1", "session1", "extract this", image=mock_image))
        self.assertIn("Spring Concert", result)

    @patch("flyer_updater.agents.agent._get_runner_and_session")
    def test_query_agent_with_audio(self, mock_get_runner_and_session):
        mock_runner = MagicMock()
        mock_get_runner_and_session.return_value = (mock_runner, MagicMock())

        mock_event = MagicMock()
        mock_event.is_final_response.return_value = True
        mock_event.content.parts = [MagicMock(text="Department is CS")]

        async def fake_run(**_):
            yield mock_event

        mock_runner.run_async = fake_run

        mock_audio = MagicMock()
        mock_audio.getvalue.return_value = b"fake_audio_bytes"
        mock_audio.type = "audio/wav"

        result = str(agent_service.query_agent("user1", "session1", "listen to this", audio=mock_audio))
        self.assertIn("CS", result)

    @patch("flyer_updater.agents.agent._get_runner_and_session")
    def test_get_or_create_session_new(self, mock_get_runner_and_session):
        mock_session_service = MagicMock()
        mock_session = MagicMock()
        mock_session.id = "new-session-123"
        mock_session_service.create_session = AsyncMock(return_value=mock_session)
        mock_get_runner_and_session.return_value = (MagicMock(), mock_session_service)

        result = agent_service.get_or_create_session("user1")
        self.assertEqual(result, "new-session-123")

    def test_get_or_create_session_existing(self):
        result = agent_service.get_or_create_session("user1", "existing-session")
        self.assertEqual(result, "existing-session")


if __name__ == "__main__":
    unittest.main()
