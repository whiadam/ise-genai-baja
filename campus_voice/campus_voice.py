import streamlit as st
import pandas as pd
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


def get_report_count(issue):
    """Simple demo report count to match prototype style."""
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


# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.title("Campus Voice")
page_choice = st.sidebar.radio(
    "Go to",
    ["Home", "Trending Issues", "Map View", "Issue Details"],
    index=["Home", "Trending Issues", "Map View", "Issue Details"].index(
        st.session_state.page
    ),
)

st.session_state.page = page_choice


# -------------------------------
# HOME SCREEN
# -------------------------------
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
        if polls:
            options = [poll["poll_question"] for poll in polls]
            selected = st.selectbox("Choose a poll", options)

            if st.button("Vote"):
                st.success(f"You voted for: {selected}")
        else:
            st.write("No active polls")
    except Exception as e:
        st.error(f"Poll section error: {e}")

    st.subheader("Facility Ratings")
    try:
        ratings = get_facility_ratings()
        if ratings:
            for r in ratings[:5]:
                st.write(f"- {r['facility_name']}: {r['rating']}/5 — {r['comment']}")
        else:
            st.write("No ratings yet")
    except Exception as e:
        st.error(f"Ratings section error: {e}")

    st.subheader("Campus Issues")
    try:
        min_rating = st.selectbox("Show issues with rating at least", [1, 2, 3, 4, 5])
        issues = get_filtered_issues(min_rating)

        if issues:
            for issue in issues[:5]:
                st.write(f"### {issue['title']}")
                st.write(issue["description"])
                st.caption(f"Rating: {issue['rating']} | Time: {issue['timestamp']}")
        else:
            st.write("No issues found")
    except Exception as e:
        st.error(f"Issues section error: {e}")


# -------------------------------
# TRENDING ISSUES SCREEN
# -------------------------------
elif st.session_state.page == "Trending Issues":
    st.title("Trending Issues")
    st.write("Top Issues This Week")
    st.caption("Click to view details")

    try:
        trending_issues = get_trending_issues()

        if trending_issues:
            for i, issue in enumerate(trending_issues, start=1):
                report_count = get_report_count(issue)
                button_label = f"#{i} {issue['title']} ({report_count} reports)"

                if st.button(button_label, key=f"trend_{issue['issue_id']}"):
                    st.session_state.selected_issue = issue
                    st.session_state.page = "Issue Details"
                    st.rerun()
        else:
            st.write("No trending issues right now.")
    except Exception as e:
        st.error(f"Trending section error: {e}")


# -------------------------------
# ISSUE DETAILS SCREEN
# -------------------------------
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


# -------------------------------
# MAP VIEW SCREEN
# -------------------------------
elif st.session_state.page == "Map View":
    st.title("Map View")
    st.write("This screen shows where issues are happening around campus.")

    try:
        map_issues = get_map_issues()

        if map_issues:
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
        else:
            st.write("No map issues available.")
    except Exception as e:
        st.error(f"Map section error: {e}")