#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st

def display_report_issue():
    """Display the report issue card."""
    st.subheader("Report an Issue")
    issue = st.text_area("Describe the issue (e.g., bathroom is dirty):")
    if st.button("Report Now"):
        st.success("Issue reported successfully!")

def display_rate_facility():
    """Display the rate facility card."""
    st.subheader("Rate a Facility")
    rating = st.slider("Rate (1-5 stars):", 1, 5)
    comments = st.text_area("Additional comments:")
    if st.button("Rate Now"):
        st.success("Thank you for your feedback!")

def display_vote_poll():
    """Display the vote in a poll card."""
    st.subheader("Vote in a Poll")
    options = ["Dining Hall Specials", "Campus Events", "Library Hours"]
    selected_option = st.selectbox("Choose a poll to vote on:", options)
    if st.button("Vote"):
        st.success(f"You voted for: {selected_option}")

def display_campus_buzz():
    """Display trending issues and popular polls."""
    st.subheader("Campus Buzz")
    trending_issues = ["Vending machine is broken", "Library noise complaints"]
    popular_polls = ["What food do you want this week?"]

    st.write("### Trending Issues")
    for issue in trending_issues:
        st.write(f"- {issue} [Upvote]")

    st.write("### Popular Polls")
    for poll in popular_polls:
        st.write(f"- {poll} [Upvote]")

def display_filters():
    """Display category filters."""
    st.subheader("Filters")
    filters = ["All", "Cleanliness", "Food", "Safety", "Maintenance", "Events"]
    selected_filter = st.selectbox("Select a category:", filters)

def display_app_page():
    """Displays the home page of the app."""
    st.title("Campus Voice")

    # Action Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        display_report_issue()

    with col2:
        display_rate_facility()

    with col3:
        display_vote_poll()

    display_campus_buzz()
    display_filters()


# This is the starting point for my app. I had AI help with generating some of the code since i couldn't find a streamlit format.
if __name__ == '__main__':
    display_app_page()