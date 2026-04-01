#############################################################################
# flyer_updater/flyer_landing_page.py
#############################################################################

import streamlit as st
import uuid


def render_landing_page():
    st.title("Flyer Updater")

    # Lazy-import so a missing google-adk shows a friendly error only here
    try:
        from flyer_updater.agents.agent_service import query_agent, get_or_create_session
    except ImportError as e:
        st.error(
            f"**Flyer Updater requires google-adk.**\n\n"
            f"Run `pip install google-adk>=1.0.0` in your terminal then restart the app.\n\n"
            f"Error: {e}"
        )
        return

    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if "session_id" not in st.session_state:
        st.session_state.session_id = get_or_create_session(st.session_state.user_id)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    input_method = st.radio("Take a picture or Upload a file", ["Upload", "Camera"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        if input_method == "Upload":
            image = st.file_uploader("Upload an image of a flyer", type=["png", "jpg", "jpeg"])
        else:
            image = st.camera_input("Snap a Shot")
    with col2:
        audio = st.audio_input("Speak!")

    has_media = image or audio
    if not has_media:
        st.session_state.media_submitted = False

    if has_media:
        if image and audio:
            label, display = "Process image and audio", "[Uploaded Image with Audio note]"
        elif image:
            label, display = "Extract from image", "[Uploaded Image]"
        else:
            label, display = "Process audio", "[Audio Note]"
        submit_media = st.button(label)
    else:
        submit_media = False

    chat_container = st.container()

    if submit_media:
        st.session_state.media_submitted = True
        st.session_state.messages.append({"role": "user", "content": display})
        with chat_container:
            with st.chat_message("user"):
                st.write(display)
            with st.chat_message("assistant"):
                with st.spinner("Working..."):
                    response = query_agent(
                        user_id=st.session_state.user_id,
                        session_id=st.session_state.session_id,
                        message="",
                        image=image,
                        audio=audio,
                    )
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("Upload a Photo or Audio or use the chat to create an event"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Working..."):
                    response = query_agent(
                        user_id=st.session_state.user_id,
                        session_id=st.session_state.session_id,
                        message=prompt,
                        image=image if has_media else None,
                        audio=audio if has_media else None,
                    )
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
