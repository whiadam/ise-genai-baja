import streamlit as st
from data_fetcher import get_active_polls, get_issues, get_genai_data


def campus_info_dashboard():
    """Displays the home page of the app."""
    st.title("Campus Info App")
    st.caption("Logged in as student user")
    st.divider()

    fallback_polls = [
        {"poll_question": "Should the library stay open later during midterms and finals?"},
        {"poll_question": "What food should the dining hall have more often?"},
        {"poll_question": "What kind of campus events do students want more of?"},
    ]

    fallback_issues = [
        {"title": "Dining Hall Food"},
        {"title": "Broken Vending Machine"},
        {"title": "Dirty Bathroom"},
    ]

    try:
        polls = get_active_polls()
        if not polls:
            polls = fallback_polls
    except Exception:
        polls = fallback_polls

    try:
        issues = get_issues()
        if not issues:
            issues = fallback_issues
    except Exception:
        issues = fallback_issues

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quick Poll Preview")

        seen = set()
        unique_polls = []

        for poll in polls:
            question = poll.get("poll_question", "")
            if question and question not in seen:
                seen.add(question)
                unique_polls.append(question)

        for question in unique_polls[:3]:
            st.write(f"- {question}")

    with col2:
        st.subheader("Recent Issues Preview")

        seen_issues = set()
        unique_issues = []

        for issue in issues:
            title = issue.get("title", "")
            if title and title not in seen_issues:
                seen_issues.add(title)
                unique_issues.append(title)

        for title in unique_issues[:3]:
            st.write(f"- {title}")

    st.divider()

    if st.button("Generate AI Summary"):
        with st.spinner("Generating summary..."):
            try:
                summary = get_genai_data("user1")
                st.write(summary.get("content", "No summary available."))
            except Exception:
                st.write(
                    "Campus activity is showing interest in library hours, dining hall options, "
                    "and maintenance issues like broken machines and bathroom cleanliness."
                )


campus_info_dashboard()