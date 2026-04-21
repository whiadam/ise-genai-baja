import streamlit as st
from data_fetcher import get_active_polls, get_issues, get_genai_data

def campus_info_dashboard():
    """Displays the home page of the app."""
    st.title("Campus Info App")
    st.caption("Logged in as student user")
    st.divider()

    polls = get_active_polls()
    issues = get_issues()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quick Poll Preview")
        if polls:
            for poll in polls[:3]:
                st.write(f"- {poll['poll_question']}")
        else:
            st.info("No active polls right now.")

    with col2:
        st.subheader("Recent Issues Preview")
        if issues:
            for issue in issues[:3]:
                st.write(f"- {issue['title']}")
        else:
            st.info("No recent issues right now.")

    st.divider()
    if st.button("Generate AI Summary"):
        with st.spinner("Generating summary..."):
            summary = get_genai_data('user1')
            st.write(summary["content"])
            
campus_info_dashboard()
