from vertexai.generative_models import GenerativeModel
import vertexai
from config import run_query, PROJECT_ID, DATASET, PROJECT_DATASET, VERTEX_LOCATION, MODEL_NAME

TABLE = "alerts"


def get_all_alerts():
    query = f"""
        SELECT *
        FROM `{PROJECT_DATASET}.{TABLE}`
        ORDER BY time_of_alert
    """
    return [dict(row) for row in run_query(query)]


def get_alert_by_id(alert_id):
    from google.cloud import bigquery
    query = f"""
        SELECT *
        FROM `{PROJECT_DATASET}.{TABLE}`
        WHERE alert_id = @alert_id
    """
    params = [bigquery.ScalarQueryParameter("alert_id", "INT64", alert_id)]
    results = [dict(row) for row in run_query(query, params=params)]
    return results[0] if results else None


def get_alerts_by_preference(preference):
    from google.cloud import bigquery
    query = f"""
        SELECT *
        FROM `{PROJECT_DATASET}.{TABLE}`
        WHERE @preference IN UNNEST(preference)
        ORDER BY time_of_alert
    """
    params = [bigquery.ScalarQueryParameter("preference", "STRING", preference)]
    return [dict(row) for row in run_query(query, params=params)]


def get_recurring_alerts():
    query = f"""
        SELECT *
        FROM `{PROJECT_DATASET}.{TABLE}`
        WHERE reoccuring = TRUE
        ORDER BY time_of_alert
    """
    return [dict(row) for row in run_query(query)]


def get_genai_alert_summary():
    alerts = get_all_alerts()
    alert_text = "\n".join(
        f"- {a['alert_name']} at {a['time_of_alert']} (preferences: {a['preference']})"
        for a in alerts[:10]
    )
    vertexai.init(project=PROJECT_ID, location=VERTEX_LOCATION)
    model = GenerativeModel(MODEL_NAME)
    prompt = f"Summarize these campus alerts for a student in 3-5 sentences:\n{alert_text}"
    return model.generate_content(prompt).text
