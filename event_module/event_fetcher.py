from datetime import datetime
from google.cloud import bigquery
from dataclasses import asdict
from config import run_query, get_client, PROJECT_DATASET
from event_module.event import Event 

def get_events():
    query = f"""
        SELECT * FROM `{PROJECT_DATASET}.events`
        ORDER BY time_created DESC 
    """
    return [Event(**dict(row.items())) for row in run_query(query)]

def get_upcoming_events():
    query = f"""
        SELECT * FROM `{PROJECT_DATASET}.events`
        WHERE event_starttime >= CURRENT_TIMESTAMP()
        ORDER BY event_starttime ASC
    """
    return [Event(**dict(row.items())) for row in run_query(query)]

def get_events_by_department(department):
    query = f"""
        SELECT * FROM `{PROJECT_DATASET}.events`
        WHERE department = @department
        ORDER BY time_created DESC
    """
    job_config = bigquery.QueryJobConfig(
         query_parameters=[
             bigquery.ScalarQueryParameter("department", "STRING", department)
         ]
    )
    return [Event(**dict(row.items())) for row in run_query(query, params=job_config)]

def create_event(event:Event)->int:
    table = f"`{PROJECT_DATASET}.events`"
    row = {k: v.isoformat() if isinstance(v,datetime) else v for k,v in asdict(event).items()} 
    errors = get_client().insert_rows_json(table, [row])
    if errors:
        raise Exception(f"InserFailed:{errors}")
    return event.event_id


