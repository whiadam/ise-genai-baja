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


# -------------------------------
# POLLS
# -------------------------------
def get_active_polls():
    query = f"""
        SELECT PollId, PollQuestion, CreatedAt, Category, IsActive
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_polls`
        WHERE IsActive = TRUE
        ORDER BY CreatedAt DESC
    """
    try:
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
    except Exception:
        return [
            {
                "poll_id": 1,
                "poll_question": "What campus issue should be fixed first?",
                "created_at": "2026-04-09",
                "category": "Campus Life",
                "is_active": True,
            }
        ]


# -------------------------------
# ISSUES
# -------------------------------
def get_issues():
    query = f"""
        SELECT issue_id, Title, Description, Time_stamp, Rating
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_issues`
        ORDER BY Time_stamp DESC
    """
    try:
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
    except Exception:
        return [
            {
                "issue_id": 1,
                "title": "Dirty bathroom in dorm hall",
                "description": "The bathroom has not been cleaned today.",
                "timestamp": "2026-04-09 10:00:00",
                "rating": 5,
            },
            {
                "issue_id": 2,
                "title": "Broken vending machine",
                "description": "The vending machine is not working.",
                "timestamp": "2026-04-09 09:30:00",
                "rating": 4,
            },
            {
                "issue_id": 3,
                "title": "Library AC not working",
                "description": "It is too hot in the study area.",
                "timestamp": "2026-04-08 04:00:00",
                "rating": 3,
            },
        ]


def get_filtered_issues(min_rating):
    issues = get_issues()
    return [issue for issue in issues if issue["rating"] >= min_rating]


# -------------------------------
# FACILITY RATINGS
# -------------------------------
def get_facility_ratings():
    query = f"""
        SELECT RatingId, UserId, FacilityName, Rating, Comment, CreatedAt
        FROM `{PROJECT_ID}.{DATASET}.campus_voice_facility_ratings`
        ORDER BY CreatedAt DESC
    """
    try:
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
    except Exception:
        return [
            {
                "rating_id": 1,
                "user_id": "user1",
                "facility_name": "Library",
                "rating": 4,
                "comment": "Quiet and clean.",
                "created_at": "2026-04-09 11:00:00",
            }
        ]


# -------------------------------
# GENAI SUMMARY
# -------------------------------
def get_genai_data(user_id="user1"):
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
    You are summarizing a campus feedback app.

    - Polls: {poll_count}
    - Issues: {issue_count}
    - Ratings: {rating_count}
    - Avg rating: {avg_rating:.1f}

    Give a short summary.
    """

    try:
        model = _get_genai_model()
        response = model.generate_content(prompt)
        content = response.text.strip()
    except Exception:
        content = "Campus Voice is collecting student feedback."

    return {
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# -------------------------------
# TRENDING ISSUES
# -------------------------------
def get_trending_issues():
    issues = get_issues()
    sorted_issues = sorted(
        issues,
        key=lambda issue: (issue["rating"], str(issue["timestamp"])),
        reverse=True
    )
    return sorted_issues[:5]


# -------------------------------
# MAP ISSUES
# -------------------------------
def get_map_issues():
    issues = get_issues()[:5]

    sample_locations = [
        {"lat": 38.9226, "lon": -77.0195},
        {"lat": 38.9231, "lon": -77.0210},
        {"lat": 38.9240, "lon": -77.0202},
        {"lat": 38.9218, "lon": -77.0188},
        {"lat": 38.9222, "lon": -77.0179},
    ]

    map_issues = []
    for i, issue in enumerate(issues):
        location = sample_locations[i % len(sample_locations)]
        map_issues.append({
            "issue_id": issue["issue_id"],
            "title": issue["title"],
            "description": issue["description"],
            "timestamp": issue["timestamp"],
            "rating": issue["rating"],
            "lat": location["lat"],
            "lon": location["lon"],
        })

    return map_issues