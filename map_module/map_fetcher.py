#############################################################################
# map_fetcher.py
#
# Adams Lab Functions — user profile, posts, and GenAI advice.
# Separated from data_fetcher.py and organized into map_module.
#############################################################################

from datetime import datetime
from google.cloud import bigquery
from config import run_query, PROJECT_DATASET, PROJECT_ID, VERTEX_LOCATION, MODEL_NAME


def _get_genai_model():
    import vertexai
    from vertexai.generative_models import GenerativeModel
    vertexai.init(project=PROJECT_ID, location=VERTEX_LOCATION)
    return GenerativeModel(MODEL_NAME)


def get_user_profile(user_id):
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
