from google.cloud import bigquery
from config import PROJECT_ID, DATASET,PROJECT_DATASET
from flyer_updater.flyer import Flyer


_client = None


def get_client():
    global _client
    _client = bigquery.Client()
    return _client

def get_flyers():
    query = f"SELECT * FROM `{PROJECT_DATASET}.flyer_table`"
    rows = get_client().query(query).result()
    return [Flyer(**dict(row.items())) for row in rows]

    
