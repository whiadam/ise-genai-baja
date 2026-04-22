import streamlit as st
import time
welcome_prompts=[(":material/chat:","I know about an event but don't have a flyer","no_flyer"),
                 (":material/add_a_photo:","I have a flyer   ","has_flyer"),
                 (":material/mic:","I'd rather talk it out   ","audio"),
                 ]

WELCOME_PROMPT_RESPONSES = {
    "no_flyer": {
        "action": "ask_for_details",
        "instruction": (
            "Great! To create an event without a flyer, I need: "
            "event title, date, start time, location, and department. "
            "Tell me what you know and I'll follow up on the rest."
        ),
    },
    "has_flyer": {
        "action": "prompt_upload",
        "instruction": (
            "Perfect — tap the 'Upload' tab at the top of the screen "
            "and select the flyer image. I'll extract the details automatically."
        ),
    },
    "audio": {
        "action": "prompt_audio",
        "instruction": (
            "Sure! Tap the microphone icon at the bottom and describe the event "
            "however you'd like. I'll pull out the details from your recording."
        ),
    },
}
def _render_welcome_button(welcome_prompt,chat_container):
    icon,label,prompt_type = welcome_prompt
    if st.button(label, key=f"starter_{prompt_type}",icon=icon):
        _handle_welcome_prompt_click(prompt_type,label,chat_container)

def render_welcome_prompts(chat_container):
    with chat_container:
        if not st.session_state.messages:
            with st.container(key="welcome_prompt_container"):
                for prompt in welcome_prompts:
                    _render_welcome_button(prompt,chat_container)

def _handle_welcome_prompt_click(prompt_type, label, chat_container):
    
    response = WELCOME_PROMPT_RESPONSES[prompt_type]["instruction"]
    
    st.session_state.messages.append({"role": "user", "content": label})
    st.session_state.messages.append({"role": "assistant", "content": response})
    with chat_container:
        with st.chat_message("user"):
            st.write(label)
        with st.chat_message("assistant"):

            st.write_stream(_stream_writer(response), cursor="...")
    st.session_state.pending_welcome_context = (
        f"The user clicked the '{prompt_type}' welcome prompt and was given "
        f"instructions. They'll now respond with event details."
    )
    
    st.rerun()

def _stream_writer(response):
    for letter in response:
        yield letter
        time.sleep(0.01)
