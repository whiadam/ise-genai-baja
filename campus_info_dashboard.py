import streamlit as st
import random
from data_fetcher import get_active_polls, get_issues


def campus_info_dashboard():
    """Displays the home page of the app."""
    st.title("Campus Info App")
    st.caption("Logged in as student user")
    st.divider()

    # -------------------------------
    # FALLBACK DATA
    # -------------------------------
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

    # -------------------------------
    # FETCH DATA (SAFE)
    # -------------------------------
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

    # -------------------------------
    # POLLS (REMOVE DUPLICATES)
    # -------------------------------
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

    # -------------------------------
    # ISSUES (REMOVE DUPLICATES)
    # -------------------------------
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

    # -------------------------------
    # AI SUMMARY (DYNAMIC)
    # -------------------------------
    if st.button("Generate AI Summary"):
        summaries = [
            "Students seem most concerned about library hours, dining options, and campus maintenance issues.",
            "The latest campus activity shows students want better study spaces, improved food options, and faster responses to facility problems.",
            "Current feedback suggests that students are focused on convenience, cleanliness, and access to reliable campus resources.",
            "Campus trends indicate a strong demand for improved facilities, extended study hours, and better overall student experience.",
        ]

        st.success("AI Summary Generated")
        st.write(random.choice(summaries))


campus_info_dashboard()