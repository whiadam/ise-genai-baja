import streamlit as st
from data_fetcher import get_active_polls, get_filtered_issues, get_facility_ratings

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
except Exception:
    polls = []
    st.error("Could not load polls. BigQuery permissions may still need to be updated.")

if polls:
    options = [poll["poll_question"] for poll in polls]
    selected = st.selectbox("Choose a poll", options)

    if st.button("Vote"):
        st.success(f"You voted for: {selected}")
else:
    st.write("No active polls")

st.subheader("Facility Ratings")

try:
    ratings = get_facility_ratings()
except Exception:
    ratings = []
    st.error("Could not load ratings. BigQuery permissions may still need to be updated.")

if ratings:
    for r in ratings[:5]:
        st.write(f"- {r['facility_name']}: {r['rating']}/5 — {r['comment']}")
else:
    st.write("No ratings yet")

st.subheader("Campus Issues")

min_rating = st.selectbox("Show issues with rating at least", [1, 2, 3, 4, 5])

try:
    issues = get_filtered_issues(min_rating)
except Exception:
    issues = []
    st.error("Could not load issues. BigQuery permissions may still need to be updated.")

if issues:
    for issue in issues[:5]:
        st.write(f"### {issue['title']}")
        st.write(issue["description"])
        st.caption(f"Rating: {issue['rating']} | Time: {issue['timestamp']}")
else:
    st.write("No issues found")