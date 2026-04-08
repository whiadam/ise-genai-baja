import time
import streamlit as st
import uuid
from flyer_updater.agents.agent_service import query_agent, get_or_create_session

STYLE=f"""
    <style>
        [data-testid="stAppViewContainer"]{{
             background-color: #ffffff;
        }}
        .st-key-chat_container{{
            border: none;
            border-radius: 10px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        }}
        .st-key-input_container{{
            border: none;
            border-radius: 0px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }}
        .st-key-page_container{{
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            border-radius: 10px;
        }}
        .st-key-camera,.st-key-upload{{
            background: #8f283a;
            margin-top: -15px;
            margin-bottom: -125px;
            border-radius: 0px;
        }}
        .st-key-landing_page_container{{
            background: linear-gradient(to top, #110b16, #8f283a);
            border-radius: 0px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            gap:0px;
        }}
        .st-key-header{{
            text-shadow:2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom:-45px;
        }}
        .st-key-top{{
            text-align: center;
            color: #D3AF37;
            background: linear-gradient(to top, #8f283a, #8f283a);
            padding: 10px;
            margin-bottom:-20px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }}
    </style>
"""

def render_landing_page():
    st.html(STYLE)

    if "media_key" not in st.session_state:
        st.session_state.media_key = 0
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if "session_id" not in st.session_state:
        st.session_state.session_id = get_or_create_session(st.session_state.user_id)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_image" not in st.session_state:
        st.session_state.pending_image = None
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = 0

    k = st.session_state.media_key
    image = None

    with st.container(key="page_container"):
        with st.container(key="top"):
            with st.container(key="header", gap=None, horizontal_alignment="center"):
                st.header("Event Creation Assistant", text_alignment="center")
            with st.container(key="selector_container", horizontal_alignment="center"):
                input_selector = st.radio("", ["Chat", "Camera", "Upload"], key=f"selected_tab_{k}",
                                          horizontal=True, index=st.session_state.active_tab)
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
