import streamlit as st
from data_fetcher import (
    get_active_polls,
    get_issues,
    get_filtered_issues,
    get_facility_ratings,
)

st.title("Campus Voice")

st.subheader("Report an Issue")
issue_title = st.text_input("Issue title")
issue_description = st.text_area("Describe the issue")
issue_rating = st.slider("How serious is it? (1-5)", 1, 5)

if st.button("Report Now"):
    if issue_title.strip() and issue_description.strip():
        st.success("Issue submitted to the app flow.")
    else:
        st.warning("Please enter both a title and description.")

st.subheader("Vote in a Poll")
polls = get_active_polls()
if polls:
    poll_options = [poll["poll_question"] for poll in polls]
    selected_poll = st.selectbox("Choose a poll", poll_options)
    if st.button("Vote"):
        st.success(f"You voted for: {selected_poll}")
else:
    st.info("No active polls right now.")

st.subheader("Facility Ratings")
ratings = get_facility_ratings()
if ratings:
    for rating in ratings[:5]:
        st.write(
            f"- {rating['facility_name']}: {rating['rating']}/5 — {rating['comment']}"
        )
else:
    st.write("No ratings yet.")

st.subheader("Campus Issues")
min_rating = st.selectbox("Show issues with rating at least", [1, 2, 3, 4, 5])

filtered_issues = get_filtered_issues(min_rating)

if filtered_issues:
    for issue in filtered_issues[:5]:
        st.write(f"### {issue['title']}")
        st.write(issue["description"])
        st.caption(f"Rating: {issue['rating']} | Timestamp: {issue['timestamp']}")
else:
    st.write("No issues match this filter.")