# create_events.py

from datetime import datetime

# simple in-memory storage (temporary)
EVENTS_DB = []


def create_event(title, description, location, event_type, department):
    """
    Create a new event and store it
    """

    if not title or not location:
        raise ValueError("Title and location are required")

    event_id = len(EVENTS_DB) + 1

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

    EVENTS_DB.append(event)
    return event


def get_events():
    """
    Return all events
    """
    return EVENTS_DB


def get_event_by_id(event_id):
    """
    Find event by ID
    """
    for event in EVENTS_DB:
        if event["event_id"] == event_id:
            return event
    return None


def rsvp_event(event_id):
    """
    Increment RSVP count
    """
    event = get_event_by_id(event_id)

    if event is None:
        raise ValueError("Event not found")

    event["rsvp_count"] += 1
    return event


def clear_events():
    """
    ONLY for testing (resets DB)
    """
    EVENTS_DB.clear()
