import time
import streamlit as st
import uuid
from flyer_updater.agents.agent_service import query_agent, get_or_create_session
from flyer_updater.flyer_style import STYLE
from flyer_updater.flyer_welcome_prompt import render_welcome_prompts
from flyer_updater.flyer_event_form import render_event_form


def render_landing_page():
    st.html(STYLE)
    _init_session_state()
    # DEV: force form open for styling work
    if st.session_state.event_form_key==0:
        st.session_state.pending_event = {
            "event_title": "Spring Career Fair",
            "event_location": "Bryan Center",
            "event_startime": "2026-05-15 14:00:00",
            "event_endtime": "2026-05-15 16:00:00",
            "department": "Career Services",
            "description": "Meet recruiters from top tech companies.",
            "creator": "career_services",
            "confidence_scores": {
                "event_title": 92,
                "event_location": 65,      # <-- low, will show ⚠️
                "event_startime": 88,
                "event_endtime": 45,        # <-- low, will show ⚠️
                "department": 78,
                "description": 82,
            },
        }
        st.session_state.original_extraction = dict(st.session_state.pending_event)

    with st.container(key="page_container"):
        input_mode = _render_top_selector()
        _render_media_input(input_mode)
        chat_container, prompt = _render_chat_area()
        render_welcome_prompts(chat_container)
        render_event_form()
        if prompt:
            _process_agent_query(chat_container, prompt=prompt)
        handle_pending_media(chat_container)


def _init_session_state():
    defaults = {
        "media_key": 0,
        "messages": [],
        "pending_image": None,
        "pending_audio": None,
        "active_tab": 0,
        "pending_event": None,
        "original_extraction": None,
        "event_form_key": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if "session_id" not in st.session_state:
        st.session_state.session_id = get_or_create_session(st.session_state.user_id)


def _render_top_selector():
    with st.container(key="top"):
        with st.container(key="header", gap=None, horizontal_alignment="center"):
            st.header("Event Creation Assistant", text_alignment="center")
        with st.container(key="selector_container", horizontal_alignment="center"):
            return st.radio(
                "Input Mode",
                ["Chat", "Camera", "Upload"],
                key=f"selected_tab_{st.session_state.media_key}",
                horizontal=True,
                index=st.session_state.active_tab,
                label_visibility="collapsed",
            )


def _render_media_input(input_mode):
    k = st.session_state.media_key
    image = None
    if input_mode == "Camera":
        with st.container(key="camera"):
            image = st.camera_input(
                "Snap a Shot \U0001F4F8", key=f"camera_image_upload_{k}"
            )
    elif input_mode == "Upload":
        with st.container(key="upload"):
            image = st.file_uploader(
                "Upload an image of a flyer",
                type=["png", "jpg", "jpeg"],
                key=f"file_image_upload_{k}",
            )
    st.session_state.pending_image = image


def _render_chat_area():
    with st.container(key="landing_page_container", gap="xxsmall"):
        chat_container = st.container(key="chat_container", height=350, gap="xxsmall")
        with chat_container:
            _render_message_history()

        input_container = st.container(
            key="input_container",
            height=200,
            vertical_alignment="center",
            horizontal_alignment="center",
            gap="small",
        )

        with input_container:
            prompt = st.chat_input("Describe an Event!")
            audio = st.audio_input(
                "Record Audio note",
                key=f"audio_file_upload_{st.session_state.media_key}",
                label_visibility="collapsed",
            )
            st.session_state.pending_audio = audio

    return chat_container, prompt


def _render_message_history():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], width="content"):
            st.write(msg["content"])


def _process_agent_query(chat_container, prompt=None, image=None, audio=None, display=None):
    welcome_context = st.session_state.pop("pending_welcome_context", None)
    message_to_agent = prompt or ""
    if welcome_context:
        message_to_agent = f"[Context: {welcome_context}]\n\n{message_to_agent}"

    st.session_state.messages.append({"role": "user", "content": display or prompt})
    with chat_container:
        with st.chat_message("user", width="content"):
            st.write(display or prompt)
        with st.chat_message("assistant"):
            with st.spinner("Working..."):
                try:
                    response = query_agent(
                        user_id=st.session_state.user_id,
                        session_id=st.session_state.session_id,
                        message=message_to_agent,
                        image=image,
                        audio=audio,
                    )
                except Exception as e:
                    response = (
                        "Something went wrong talking to the agent. "
                        "Try again in a moment. "
                        f"(Error: {type(e).__name__})"
                    )
            st.write_stream(_stream_writer(response), cursor="...")
            st.session_state.messages.append({"role": "assistant", "content": response})


def handle_pending_media(chat_container):
    if not (st.session_state.pending_image or st.session_state.pending_audio):
        return
    pending_image = st.session_state.pop("pending_image", None)
    pending_audio = st.session_state.pop("pending_audio", None)
    display = _format_media_display(pending_image, pending_audio)
    st.session_state.media_key += 1
    st.session_state.active_tab = 0
    _process_agent_query(chat_container, image=pending_image, audio=pending_audio, display=display)
    st.rerun()


def _format_media_display(image, audio):
    if image and audio:
        return "[Uploaded Image with Audio note]"
    elif image:
        return "[Uploaded Image]"
    else:
        return "[Audio Note]"


def _stream_writer(response):
    for letter in response:
        yield letter
        time.sleep(0.01)
