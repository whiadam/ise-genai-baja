import streamlit as st
import pandas as pd

try:
    from campus_voice.data_fetcher import (
        get_active_polls,
        get_filtered_issues,
        get_facility_ratings,
        get_trending_issues,
        get_map_issues,
    )
except ModuleNotFoundError:
    from data_fetcher import (
        get_active_polls,
        get_filtered_issues,
        get_facility_ratings,
        get_trending_issues,
        get_map_issues,
    )

st.set_page_config(page_title="Campus Voice", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "selected_issue" not in st.session_state:
    st.session_state.selected_issue = None


def remove_duplicates(items, key):
    seen = set()
    unique_items = []

    for item in items:
        value = item.get(key, "")
        if value and value not in seen:
            seen.add(value)
            unique_items.append(item)

    return unique_items


def get_report_count(issue):
    rating = issue.get("rating", 1)
    if rating == 5:
        return 20
    if rating == 4:
        return 15
    if rating == 3:
        return 8
    if rating == 2:
        return 5
    return 3


fallback_polls = [
    {"poll_question": "Should the library stay open later during midterms and finals?"},
    {"poll_question": "What food should the dining hall have more often?"},
    {"poll_question": "What kind of campus events do students want more of?"},
]

fallback_ratings = [
    {"facility_name": "Gym", "rating": 4, "comment": "Good equipment but it gets crowded."},
    {"facility_name": "Dining Hall", "rating": 3, "comment": "The food is okay but could be better."},
    {"facility_name": "Library", "rating": 5, "comment": "Great study space during exams."},
]

fallback_issues = [
    {
        "issue_id": "1",
        "title": "Dining Hall Food",
        "description": "Students want more food options.",
        "rating": 4,
        "timestamp": "2026-04-24",
        "lat": 36.001,
        "lon": -78.938,
    },
    {
        "issue_id": "2",
        "title": "Broken Vending Machine",
        "description": "Machine on 2nd floor is not working.",
        "rating": 3,
        "timestamp": "2026-04-24",
        "lat": 36.002,
        "lon": -78.939,
    },
    {
        "issue_id": "3",
        "title": "Dirty Bathroom",
        "description": "Bathroom needs cleaning.",
        "rating": 5,
        "timestamp": "2026-04-24",
        "lat": 36.003,
        "lon": -78.940,
    },
]


st.sidebar.title("Campus Voice")
page_choice = st.sidebar.radio(
    "Go to",
    ["Home", "Trending Issues", "Map View", "Issue Details"],
    index=["Home", "Trending Issues", "Map View", "Issue Details"].index(
        st.session_state.page
    ),
)

st.session_state.page = page_choice


if st.session_state.page == "Home":
    st.title("Campus Voice")

    st.subheader("Report an Issue")
    title = st.text_input("Issue title")
    description = st.text_area("Describe the issue")
    rating = st.slider("How serious is it? (1-5)", 1, 5)

    if st.button("Report Now"):
        if title and description:
            st.success("Issue submitted!")
        else:
            st.warning("Please fill everything out")

    st.subheader("Vote in a Poll")
    try:
        polls = get_active_polls()
        if not polls:
            polls = fallback_polls
    except Exception:
        polls = fallback_polls

    polls = remove_duplicates(polls, "poll_question")
    poll_options = [poll["poll_question"] for poll in polls]

    selected = st.selectbox("Choose a poll", poll_options)

    if st.button("Vote"):
        st.success(f"You voted for: {selected}")

    st.subheader("Facility Ratings")
    try:
        ratings = get_facility_ratings()
        if not ratings:
            ratings = fallback_ratings
    except Exception:
        ratings = fallback_ratings

    seen_ratings = set()
    unique_ratings = []

    for r in ratings:
        rating_text = f"{r.get('facility_name')}: {r.get('rating')}/5 — {r.get('comment')}"
        if rating_text not in seen_ratings:
            seen_ratings.add(rating_text)
            unique_ratings.append(rating_text)

    for rating_text in unique_ratings[:5]:
        st.write(f"- {rating_text}")

    st.subheader("Campus Issues")
    min_rating = st.selectbox("Show issues with rating at least", [1, 2, 3, 4, 5])

    try:
        issues = get_filtered_issues(min_rating)
        if not issues:
            issues = fallback_issues
    except Exception:
        issues = fallback_issues

    issues = [issue for issue in issues if issue.get("rating", 1) >= min_rating]
    issues = remove_duplicates(issues, "title")

    for issue in issues[:5]:
        st.write(f"### {issue['title']}")
        st.write(issue["description"])
        st.caption(f"Rating: {issue['rating']} | Time: {issue['timestamp']}")


elif st.session_state.page == "Trending Issues":
    st.title("Trending Issues")
    st.write("Top Issues This Week")
    st.caption("Click to view details")

    try:
        trending_issues = get_trending_issues()
        if not trending_issues:
            trending_issues = fallback_issues
    except Exception:
        trending_issues = fallback_issues

    trending_issues = remove_duplicates(trending_issues, "title")

    for i, issue in enumerate(trending_issues, start=1):
        report_count = get_report_count(issue)
        button_label = f"#{i} {issue['title']} ({report_count} reports)"

        if st.button(button_label, key=f"trend_{issue['issue_id']}"):
            st.session_state.selected_issue = issue
            st.session_state.page = "Issue Details"
            st.rerun()


elif st.session_state.page == "Issue Details":
    st.title("Issue Details")

    issue = st.session_state.selected_issue

    if issue:
        st.write(f"## {issue['title']}")
        st.write("**Description:**")
        st.write(issue["description"])
        st.write(f"**Rating:** {issue['rating']}/5")
        st.write(f"**Time:** {issue['timestamp']}")

        st.write("### Rate how bad or serious the problem is")
        st.write("⭐ = not a big deal")
        st.write("⭐⭐⭐ = kinda annoying")
        st.write("⭐⭐⭐⭐⭐ = needs fixing ASAP / terrible")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Back to Trending Issues"):
                st.session_state.page = "Trending Issues"
                st.rerun()

        with col2:
            if st.button("Map"):
                st.session_state.page = "Map View"
                st.rerun()
    else:
        st.write("No issue selected yet.")
        if st.button("Go to Trending Issues"):
            st.session_state.page = "Trending Issues"
            st.rerun()


elif st.session_state.page == "Map View":
    st.title("Map View")
    st.write("This screen shows where issues are happening around campus.")

    try:
        map_issues = get_map_issues()
        if not map_issues:
            map_issues = fallback_issues
    except Exception:
        map_issues = fallback_issues

    map_issues = remove_duplicates(map_issues, "title")

    map_data = pd.DataFrame(
        [{"lat": issue["lat"], "lon": issue["lon"]} for issue in map_issues]
    )
    st.map(map_data)

    st.write("### Issue Locations")
    st.caption("Click to view details")

    for issue in map_issues:
        report_count = get_report_count(issue)
        button_label = f"{issue['title']} ({report_count} reports)"

        if st.button(button_label, key=f"map_{issue['issue_id']}"):
            st.session_state.selected_issue = issue
            st.session_state.page = "Issue Details"
            st.rerun()