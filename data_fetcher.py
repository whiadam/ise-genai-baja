#############################################################################
# data_fetcher.py
#
# BigQuery + Vertex AI data fetcher for Campus Voice
#############################################################################

from datetime import datetime
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel
from config import (
    get_client,
    run_query,
    PROJECT_ID,
    PROJECT_DATASET,
    VERTEX_LOCATION,
    MODEL_NAME,
)

# Create the BigQuery client once
client = get_client()


def _get_genai_model():
    vertexai.init(project=PROJECT_ID, location=VERTEX_LOCATION)
    return GenerativeModel(MODEL_NAME)


def get_active_polls():
    """Returns active polls from the database."""
    query = f"""
        SELECT PollId, PollQuestion, CreatedAt, Category, IsActive
        FROM `{PROJECT_DATASET}.campus_voice_polls`
        WHERE IsActive = TRUE
        ORDER BY CreatedAt DESC
    """
    rows = run_query(query) 

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


def get_issues():
    """Returns all campus issues from the database."""
    query = f"""
        SELECT issue_id, Title, Description, Time_stamp, Rating
        FROM `{PROJECT_DATASET}.campus_voice_issues`
        ORDER BY Time_stamp DESC
    """
    rows = run_query(query) 

    issues = []
    for row in rows:
        issues.append({
            "issue_id": row.issue_id,
            "title": row.Title,
            "description": row.Description,
            "timestamp": row.Time_stamp,
            "rating": row.Rating,
        })
    return issues


def get_filtered_issues(min_rating):
    """Returns issues with a rating greater than or equal to the given value."""
    query = f"""
        SELECT issue_id, Title, Description, Time_stamp, Rating
        FROM `{PROJECT_DATASET}.campus_voice_issues`
        WHERE Rating >= @min_rating
        ORDER BY Time_stamp DESC
    """

    params = [  bigquery.ScalarQueryParameter("min_rating", "INT64", min_rating)]
    rows = run_query(query, params=params )

    issues = []
    for row in rows:
        issues.append({
            "issue_id": row.issue_id,
            "title": row.Title,
            "description": row.Description,
            "timestamp": row.Time_stamp,
            "rating": row.Rating,
        })
    return issues


def get_facility_ratings():
    """Returns facility ratings from the database."""
    query = f"""
        SELECT RatingId, UserId, FacilityName, Rating, Comment, CreatedAt
        FROM `{PROJECT_DATASET}.campus_voice_facility_ratings`
        ORDER BY CreatedAt DESC
    """
    rows = run_query(query)

    ratings = []
    for row in rows:
        ratings.append({
            "rating_id": row.RatingId,
            "user_id": row.UserId,
            "facility_name": row.FacilityName,
            "rating": row.Rating,
            "comment": row.Comment,
            "created_at": row.CreatedAt,
        })
    return ratings


def get_genai_data(user_id="user1"):
    """Uses Vertex AI to generate a short Campus Voice summary based on DB data."""
    polls = get_active_polls()
    issues = get_issues()
    ratings = get_facility_ratings()

    issue_count = len(issues)
    poll_count = len(polls)
    rating_count = len(ratings)
    avg_rating = (
        sum(r["rating"] for r in ratings) / rating_count
        if rating_count else 0
    )

    prompt = f"""
    You are helping summarize activity in a student campus feedback app called Campus Voice.

    Current data:
    - Active polls: {poll_count}
    - Reported issues: {issue_count}
    - Facility ratings submitted: {rating_count}
    - Average facility rating: {avg_rating:.1f}

    Write a short, student-friendly summary in 2-3 sentences.
    Mention one useful next step the app should encourage students to take.
    """

    try:
        model = _get_genai_model()
        content = model.generate_content(prompt).text.strip()
    except Exception:
        content = (
            "Campus Voice is collecting student feedback through polls, issue reports, "
            "and facility ratings. A good next step is encouraging more students to vote "
            "in active polls and report campus issues."
        )

    return {
        "advice_id": "genai1",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": content,
        "image": None,
    }


def get_trending_issues():
    """Returns top trending issues using highest ratings."""
    issues = get_issues()
    return sorted(issues, key=lambda x: x["rating"], reverse=True)[:5]


def get_map_issues():
    """Returns issues with demo coordinates for map display."""
    issues = get_issues()

    for i, issue in enumerate(issues):
        issue["lat"] = 38.92 + (i * 0.001)
        issue["lon"] = -77.02 + (i * 0.001)

    return issues

# ---------------------------------------------------------------------------
# Adams Lab Functions
# ---------------------------------------------------------------------------

def get_user_profile(user_id):
    from google.cloud import bigquery
    query = f"""
        SELECT u.full_name, u.username, u.date_of_birth, u.profile_image,
               ARRAY_AGG(f.friend_user_id IGNORE NULLS) AS friends
        FROM `{PROJECT_DATASET}.users` u
        LEFT JOIN `{PROJECT_DATASET}.friends` f ON u.user_id = f.user_id
        WHERE u.user_id = @user_id
        GROUP BY u.full_name, u.username, u.date_of_birth, u.profile_image
    """
    params = [bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    rows = list(run_query(query, params=params))
    if not rows:
        return None
    row = rows[0]
    return {
        "full_name":     row.full_name,
        "username":      row.username,
        "date_of_birth": str(row.date_of_birth),
        "profile_image": row.profile_image,
        "friends":       list(row.friends) if row.friends else [],
    }


def get_user_posts(user_id):
    from google.cloud import bigquery
    query = f"""
        SELECT user_id, post_id, timestamp, content, image
        FROM `{PROJECT_DATASET}.posts`
        WHERE user_id = @user_id
        ORDER BY timestamp DESC
    """
    params = [bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
    posts = []
    for row in run_query(query, params=params):
        posts.append({
            "user_id":   row.user_id,
            "post_id":   row.post_id,
            "timestamp": str(row.timestamp),
            "content":   row.content,
            "image":     row.image,
        })
    return posts


def get_genai_advice(user_id):
    profile = get_user_profile(user_id)
    if not profile:
        return {
            "advice_id": "genai-advice-1",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content":   "No user profile found. Visit the campus map to explore events near you!",
            "image":     None,
        }
    prompt = f"""
    You are a helpful campus advisor for a student events app.
    Based on this user:
    - Name: {profile['full_name']}
    - Username: {profile['username']}
    - Friends count: {len(profile['friends'])}
    Write one short friendly tip (1-2 sentences) about exploring campus events or inviting friends.
    """
    try:
        model   = _get_genai_model()
        content = model.generate_content(prompt).text.strip()
    except Exception:
        content = "Check the campus map for events near you and invite a friend to join!"
    return {
        "advice_id": "genai-advice-1",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content":   content,
        "image":     None,
    }
