import json
from dataclasses import asdict
from datetime import datetime
from config import get_client,run_query,PROJECT_DATASET
from flyer_updater.flyer import Flyer

def get_flyers():
    query = f"SELECT * FROM `{PROJECT_DATASET}.flyer_table`"
    return [Flyer(**dict(row.items())) for row in run_query(query)]

def create_flyer(flyer:Flyer)-> int:
    table = f"`{PROJECT_DATASET}.flyer_table`"
    row = {k: v.isoformat() if isinstance(v,datetime) else v for k, v in asdict(flyer).items()}
    if row.get("confidence_Scores"):
        row["confidence_scores"] = json.dumps(row["confidence_scores"])
    errors = get_client().insert_rows_json(table,[row])
    if errors:
        raise Exception(f"Insert failed: {errors}")
    return flyer.flyer_id


    
