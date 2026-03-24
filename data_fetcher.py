#############################################################################
# data_fetcher.py
#
# BigQuery + Vertex AI data fetcher for Campus Voice
#############################################################################

from datetime import datetime
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "jeffrey-perparas-csu-fullerton"
DATASET = "campus_event_tracker"
VERTEX_LOCATION = "us-central1"
MODEL_NAME = "gemini-2.0-flash"

client = bigquery.Client(project=PROJECT_ID)


def _get_genai_model():
    vertexai.init(project=PROJECT_ID, location=VERTEX_LOCATION)
    return GenerativeModel(MODEL_NAME)


def get_active_polls():
    """Returns active polls from the database."""
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


def get_issues():
    """Returns all campus issues from the database."""
    query = f"""
        SELECT issue_id, Title, Description, Time_stamp, Rating
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_issues`
        ORDER BY Time_stamp DESC
    """
    rows = client.query(query).result()

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
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_issues`
        WHERE Rating >= @min_rating
        ORDER BY Time_stamp DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("min_rating", "INT64", min_rating)
        ]
    )

    rows = client.query(query, job_config=job_config).result()

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
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_facility_ratings`
        ORDER BY CreatedAt DESC
    """
    rows = client.query(query).result()

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

    avg_rating = 0
    if rating_count > 0:
        avg_rating = sum(r["rating"] for r in ratings) / rating_count

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
        response = model.generate_content(prompt)
        content = response.text.strip()
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