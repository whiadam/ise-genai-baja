#############################################################################
# flyer_updater/agents/agent_service.py
#############################################################################

import asyncio
import base64
from google.genai import types


def get_or_create_session(user_id, session_id=None):
    """Create an ADK session for the given user, or return the existing one."""
    if session_id:
        return session_id

    from flyer_updater.agents.agent import _get_runner_and_session
    _, session_service = _get_runner_and_session()

    async def _create():
        session = await session_service.create_session(
            app_name="flyer_updater",
            user_id=user_id,
        )
        return session.id

    return asyncio.run(_create())


def query_agent(user_id, session_id, message, image=None, audio=None):
    """Send a message (optionally with image / audio) to the flyer agent.

    Args:
        user_id:    the user's id
        session_id: ADK in-memory session id
        message:    text prompt
        image:      Streamlit UploadedFile / camera_input
        audio:      Streamlit audio_input
    """
    from flyer_updater.agents.agent import _get_runner_and_session
    runner, _ = _get_runner_and_session()

    parts = []
    if image:
        parts.append(types.Part.from_bytes(
            data=image.getvalue(),
            mime_type=image.type,
        ))
    if audio:
        parts.append(types.Part.from_bytes(
            data=audio.getvalue(),
            mime_type=audio.type,
        ))
    parts.append(types.Part(text=message))

    content = types.Content(role="user", parts=parts)

    async def _run():
        response = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response = event.content.parts[0].text
        return response

    return asyncio.run(_run())
