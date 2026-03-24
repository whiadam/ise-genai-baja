from google.cloud import bigquery
from config import get_client,PROJECT_DATASET
from flyer_updater.flyer import Flyer

def get_flyers():
    query = f"SELECT * FROM `{PROJECT_DATASET}.flyer_table`"
    rows = get_client().query(query).result()
    return [Flyer(**dict(row.items())) for row in rows]

    
