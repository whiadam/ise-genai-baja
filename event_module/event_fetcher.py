from google.cloud import bigquery
from config import run_query,PROJECT_DATASET
from event_module.event import Event 

def get_events():
    query = f"""
        SELECT * FROM `{PROJECT_DATASET}.events`
        ORDER BY time_created DESC 
    """
    return [Event(**dict(row.items())) for row in run_query(query)]

def get_upcomming_events():
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
    return [Event(**dict(row.items())) for row in run_query(query, job_config=job_config)]

