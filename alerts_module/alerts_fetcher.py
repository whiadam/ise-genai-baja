from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "jeffrey-perparas-csu-fullerton"
DATASET = "campus_event_tracker"
TABLE = "alerts"

def get_bigquery_client():
    return bigquery.Client(project=PROJECT_ID)

def get_all_alerts():
    client = get_bigquery_client()
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        ORDER BY time_of_alert
    """
    return [dict(row) for row in client.query(query).result()]

def get_alert_by_id(alert_id):
    client = get_bigquery_client()
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE alert_id = @alert_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("alert_id", "INT64", alert_id)
        ]
    )
    results = [dict(row) for row in client.query(query, job_config=job_config).result()]
    return results[0] if results else None

def get_alerts_by_preference(preference):
    client = get_bigquery_client()
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE @preference IN UNNEST(preference)
        ORDER BY time_of_alert
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("preference", "STRING", preference)
        ]
    )
    return [dict(row) for row in client.query(query, job_config=job_config).result()]

def get_recurring_alerts():
    client = get_bigquery_client()
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE reoccuring = TRUE
        ORDER BY time_of_alert
    """
    return [dict(row) for row in client.query(query).result()]

def get_genai_alert_summary():
    alerts = get_all_alerts()
    alert_text = "\n".join(
        f"- {alert['alert_name']} at {alert['time_of_alert']} (preferences: {alert['preference']})"
        for alert in alerts[:10]
    )

    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Summarize these campus alerts for a student in 3-5 sentences:
    {alert_text}
    """

    response = model.generate_content(prompt)
    return response.text