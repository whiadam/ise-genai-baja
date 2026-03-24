from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    event_id: int
    time_created: datetime
    creator: str
    event_startime: Optional[datetime] = None
    event_endtime: Optional[datetime] = None
    event_title: Optional[str] = None
    event_location: Optional[str] = None
    department: Optional[str] = None 
    description: Optional[str] = None
