import asyncio
import base64
from google.genai import types
from flyer_updater.agents.agent import runner, session_service

async def _create_session(user_id):
    session = await session_service.create_session(
            app_name="flyer_updater",
            user_id=user_id
            )
    return session.id

def get_or_create_session(user_id, session_id=None):
    if session_id:
        return session_id
    return asyncio.run(_create_session(user_id))

def query_agent(user_id,session_id, message, image=None, audio=None):
    """Send a message to the flyer agent, with image or audio
    Args:
        user_id: the user's id (we don't have auth so its hard coded)
        session_id: uses Google ADK to create an in memory session
        image: uploaded from streamlit camera or input
        audio: Streamlit audio input
    """
    parts =[]

    if image:
        parts.append(types.Part.from_bytes(
            data=image.getvalue(),
            mime_type=image.type
            ))
    if audio:
        parts.append(types.Part.from_bytes(
            data=audio.getvalue(),
            mime_type=audio.type
            ))
    parts.append(types.Part(text=message))

    content = types.Content(role="user", parts=parts)

    async def _run():
        response = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    response = event.content.parts[0].text
        return response
    
    return asyncio.run(_run())
                    
