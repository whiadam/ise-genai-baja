import os
from google.cloud import bigquery

# ---------------------------------------------------------------------------
# Pull config from environment variables first; fall back to defaults so the
# app still runs locally without extra setup.
# ---------------------------------------------------------------------------
PROJECT_ID      = os.environ.get("GCP_PROJECT_ID",      "jeffrey-perparas-csu-fullerton")
DATASET         = os.environ.get("GCP_DATASET",         "campus_event_tracker")
VERTEX_LOCATION = os.environ.get("VERTEX_LOCATION",     "us-central1")
MODEL_NAME      = os.environ.get("GEMINI_MODEL",        "gemini-2.5-flash")
PROJECT_DATASET = f"{PROJECT_ID}.{DATASET}"

_client = None


def get_client() -> bigquery.Client:
    global _client
    if _client is None:
        _client = bigquery.Client(project=PROJECT_ID)
    return _client


def run_query(query: str, params=None):
    job_config = None
    if params:
        job_config = bigquery.QueryJobConfig(query_parameters=params)
    return get_client().query(query, job_config=job_config).result()
