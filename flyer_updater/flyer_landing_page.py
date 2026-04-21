import time
import streamlit as st
import uuid
from flyer_updater.agents.agent_service import query_agent, get_or_create_session
from flyer_updater.flyer_style import STYLE


def _init_session_state():
    defaults = {
            "media_key": 0,
            "user_id": str(uuid.uuid4()),
            "messages": [], 
            "pending_image": None,
            "active_tab":0,
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "session_id" not in st.session_state:
        st.session_state.session_id = get_or_create_session(st.session_state.user_id)

def _render_top_selector():
    with st.container(key="top"):
        with st.container(key="header", gap=None, horizontal_alignment="center"):
            st.header("Event Creation Assistant", text_alignment="center")
        with st.container(key="selector_container", horizontal_alignment="center"):
            return st.radio(
                    "", 
                    ["Chat", "Camera", "Upload"], 
                    key=f"selected_tab_{st.session_state.media_key}",
                    horizontal=True, 
                    index=st.session_state.active_tab,
                    )

def render_landing_page():
    st.html(STYLE)
    _init_session_state()


    k = st.session_state.media_key
    image = None
    input_selector = _render_top_selector()

    if input_selector == "Camera":
        with st.container(key="camera"):
            image = st.session_state.pending_image = st.camera_input(
                "Snap a Shot \U0001F4F8", key=f"camera_image_upload_{k}")
    elif input_selector == "Upload":
        with st.container(key="upload"):
            image = st.session_state.pending_image = st.file_uploader(
                "Upload an image of a flyer", type=["png", "jpg", "jpeg"], key=f"file_image_upload_{k}")

    with st.container(key="landing_page_container", gap="xxsmall"):
        chat_container = st.container(key="chat_container", height=350, gap="xxsmall")
        with chat_container:
            messages_container = st.container()

        input_container = st.container(
            key="input_container", height=200, vertical_alignment="center",
            horizontal_alignment="center", gap=None)

        with messages_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"], width="content"):
                    st.write(msg["content"])

        with input_container:
            prompt = st.chat_input("Describe an Event!")
            audio = st.session_state.pending_audio = st.audio_input("", key=f"audio_file_upload_{k}")

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user", width="content"):
                    st.write(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("Working..."):
                        response = query_agent(
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.session_id,
                            message=prompt,
                        )
                    st.write_stream(_stream_writer(response), cursor="...")
                    st.session_state.messages.append({"role": "assistant", "content": response})

        has_media = image or audio
        if has_media:
            if image and audio:
                st.session_state.pending_display = "[Uploaded Image with Audio note]"
            elif image:
                st.session_state.pending_display = "[Uploaded Image]"
            else:
                st.session_state.pending_display = "[Audio Note]"

        if st.session_state.pending_image or st.session_state.pending_audio:
            pending_image = st.session_state.pop("pending_image", None)
            pending_audio = st.session_state.pop("pending_audio", None)
            pending_display = st.session_state.pop("pending_display", None)
            st.session_state.media_key += 1
            st.session_state.active_tab = 0

            st.session_state.messages.append({"role": "user", "content": pending_display})
            with chat_container:
                with st.chat_message("user"):
                    st.write(pending_display)
                with st.chat_message("assistant"):
                    with st.spinner("Working..."):
                        response = query_agent(
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.session_id,
                            message="",
                            image=pending_image,
                            audio=pending_audio
                        )
                    st.write_stream(_stream_writer(response), cursor="...")
                    st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()


def _stream_writer(response):
    for letter in response:
        yield letter
        time.sleep(0.05)
