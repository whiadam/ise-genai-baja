from datetime import datetime
from google.cloud import bigquery
from dataclasses import asdict

from google.cloud.bigquery import query
from config import run_query, get_client, PROJECT_DATASET
from event_module.event import Event 

def get_events():
    query = f"""
        SELECT * FROM `{PROJECT_DATASET}.events`
        ORDER BY time_created DESC 
    """
    return [Event(**dict(row.items())) for row in run_query(query)]

def get_next_event_id():
    query = f"SELECT MAX(event_id)  as max_id FROM `{PROJECT_DATASET}.events`"
    result = next(run_query(query)).max_id
    return (result or 0) + 1

def get_upcoming_events():
    query = f"""
        SELECT * FROM `{PROJECT_DATASET}.events`
        WHERE event_startime >= CURRENT_TIMESTAMP()
        ORDER BY event_startime ASC
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
    if event.event_id is None:
        event.event_id = get_next_event_id()
    table = f"{PROJECT_DATASET}.events"
    row = {k: v.isoformat() if isinstance(v,datetime) else v for k,v in asdict(event).items()} 
    errors = get_client().insert_rows_json(table, [row])
    if errors:
        raise Exception(f"InserFailed:{errors}")
    return event.event_id


