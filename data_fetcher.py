#############################################################################
# data_fetcher.py
#
# This file connects the app to BigQuery and fetches real data
# for the Campus Voice app.
#############################################################################

from google.cloud import bigquery

PROJECT_ID = "jeffrey-perparas-csu-fullerton"
DATASET = "campus_event_tracker"

client = bigquery.Client(project=PROJECT_ID)


def get_user_profile(user_id):
    """Returns basic user profile info."""
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.user_data`
        LIMIT 1
    """

    rows = list(client.query(query).result())

    if not rows:
        return {
            "full_name": "Campus User",
            "username": "student",
            "date_of_birth": None,
            "profile_image": None,
            "friends": [],
        }

    row = rows[0]

    row_dict = dict(row.items())

    return {
        "full_name": row_dict.get("full_name", "Campus User"),
        "username": row_dict.get("username", "student"),
        "date_of_birth": row_dict.get("date_of_birth"),
        "profile_image": row_dict.get("profile_image"),
        "friends": row_dict.get("friends", []),
    }


def get_user_posts(user_id):
    """Returns issue reports as user posts."""
    query = f"""
        SELECT IssueId, UserId, IssueText, CreatedAt
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_issues`
        WHERE UserId = @user_id
        ORDER BY CreatedAt DESC
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )

    rows = client.query(query, job_config=job_config).result()

    posts = []
    for row in rows:
        posts.append({
            "user_id": row.UserId,
            "post_id": row.IssueId,
            "timestamp": row.CreatedAt,
            "content": row.IssueText,
            "image": None
        })

    return posts


def get_active_polls():
    """Returns active Campus Voice polls."""
    query = f"""
        SELECT PollId, PollQuestion, CreatedAt, Category, IsActive
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_polls`
        WHERE IsActive = TRUE
        ORDER BY CreatedAt DESC
    """

    rows = client.query(query).result()

    polls = []
    for row in rows:
        polls.append({
            "poll_id": row.PollId,
            "poll_question": row.PollQuestion,
            "created_at": row.CreatedAt,
            "category": row.Category,
            "is_active": row.IsActive,
        })

    return polls


def get_filtered_issues(category):
    """Returns issues for one category."""
    query = f"""
        SELECT IssueId, UserId, IssueText, Category, CreatedAt, Status
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_issues`
        WHERE Category = @category
        ORDER BY CreatedAt DESC
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("category", "STRING", category)
        ]
    )

    rows = client.query(query, job_config=job_config).result()

    issues = []
    for row in rows:
        issues.append({
            "issue_id": row.IssueId,
            "user_id": row.UserId,
            "issue_text": row.IssueText,
            "category": row.Category,
            "created_at": row.CreatedAt,
            "status": row.Status,
        })

    return issues


def get_genai_data(user_id):
    """
    Returns AI-generated advice based on Campus Voice data.
    This uses database data and generates a summary/advice-style response.
    """
    issues = get_filtered_issues("Cleanliness")
    polls = get_active_polls()

    issue_count = len(issues)
    poll_count = len(polls)

    if issue_count > 0 and poll_count > 0:
        content = (
            f"Students are actively engaging with Campus Voice. "
            f"There are currently {issue_count} cleanliness-related issues and "
            f"{poll_count} active polls. A good next step would be encouraging "
            f"students to keep reporting concerns while also using polls to prioritize fixes."
        )
    elif issue_count > 0:
        content = (
            f"There are currently {issue_count} cleanliness-related issues reported. "
            f"A useful next step would be to highlight the most common campus concerns "
            f"and encourage student feedback on solutions."
        )
    elif poll_count > 0:
        content = (
            f"There are currently {poll_count} active polls in Campus Voice. "
            f"This shows students are engaging with campus decisions, and the app can use "
            f"that feedback to improve student life."
        )
    else:
        content = (
            "Campus Voice currently has limited activity. A good next step would be to "
            "encourage students to submit issues and participate in polls."
        )

    return {
        "advice_id": "genai1",
        "timestamp": None,
        "content": content,
        "image": None
    }