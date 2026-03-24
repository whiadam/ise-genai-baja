from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Flyer:
    flyer_id: int
    upload_time: datetime
    require_user_input: Optional[bool] = None
    fields_edited: Optional[list] = None
    confidence_scores: Optional[dict] = None
    event_id: Optional[int] = None
