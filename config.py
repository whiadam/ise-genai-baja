from google.cloud import bigquery

PROJECT_ID = "jeffrey-perparas-csu-fullerton"
DATASET = "campus_event_tracker"
VERTEX_LOCATION = "us-central1"
MODEL_NAME = "gemini-2.0-flash"
PROJECT_DATASET = f"{PROJECT_ID}.{DATASET}"

_client = None

def get_client():
    global _client
    if _client is None:
        _client = bigquery.Client(project = PROJECT_ID)
    return _client
