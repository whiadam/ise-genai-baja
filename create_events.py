# create_events.py

from datetime import datetime
from data_fetcher import insert_event, get_events, update_event

# create a new event
def create_event(title, description, location, event_type, department):
    events = get_events()

    event_id = len(events) + 1  # simple ID system

    event = {
        "event_id": event_id,
        "title": title,
        "description": description,
        "location": location,
        "type": event_type,
        "department": department,
        "timestamp": datetime.utcnow().isoformat(),
        "rsvp_count": 0
    }

    insert_event(event)
    return event


# get all events
def list_events():
    return get_events()


# RSVP to event
def rsvp_event(event_id):
    events = get_events()

    for event in events:
        if event["event_id"] == event_id:
            event["rsvp_count"] += 1
            update_event(event)
            return event

    return None
