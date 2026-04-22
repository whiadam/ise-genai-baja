from datetime import datetime
import streamlit as st
from event_module.event import Event
from event_module.event_fetcher import create_event, get_upcoming_events
from flyer_updater.flyer import Flyer
from flyer_updater.flyer_fetcher import create_flyer

def preview_event(
        event_title: str,
        event_location: str,
        event_startime: str,
        event_endtime: str,
        department: str,
        description: str,
        creator: str,
        confidence_scores: dict,
    ) -> str:
    """Present extracted event details to the user for review before saving.

    Call this immediately after extracting event details from a flyer or 
    user description. Do NOT call insert_event — the UI will handle 
    submission after the user reviews and confirms the form.

    Args:
        event_title: The name of the event
        event_location: Where the event takes place
        event_startime: Start time in YYYY-MM-DD HH:MM:SS format
        event_endtime: End time in YYYY-MM-DD HH:MM:SS format
        department: The department hosting the event
        description: A brief description of the event
        creator: Who uploaded the event. Ask the user their name, put 
            anonymous if not willing.
        confidence_scores: Confidence 0-100 per field, 
            example: {"event_title": 50, "event_location": 65}

    Returns:
        Confirmation that the preview has been shown.
    """
    extracted = {
        "event_title": event_title,
        "event_location": event_location,
        "event_startime": event_startime,
        "event_endtime": event_endtime,
        "department": department,
        "description": description,
        "creator": creator,
        "confidence_scores": confidence_scores or {},
    }
    
    st.session_state.pending_event = dict(extracted)
    st.session_state.original_extraction = dict(extracted)
    
    return (
        "I've pulled out what I could. Please review the details below, "
        "make any corrections, and click 'Submit to Calendar' to save."
    )

def check_duplicate_event()->str:
    """Gets all upcoming events for duplicate checking.
        
        Returns:
            List of upcoming events with titles, locations, and startimes 
    """
    events = get_upcoming_events()
    if not events:
        return "No upcoming Events"
    return str([
        {"title": e.event_title, "location": e.event_location, "start": str(e.event_startime)}
         for e in events
     ])
def insert_event(
        event_title: str,
        event_location: str,
        event_startime: str,
        event_endtime: str,
        department: str,
        description: str,
        creator: str,
        confidence_scores: dict,
        require_user_input: bool,
        fields_edited: list,
    )->str:
    """Create an event and flyer record from extracted flyer data.
    event and flyer IDs are auto-generated *Do Not Provide ID* 

    Args:
        event_title: The name of the event
        event_location: Where the event takes place
        event_startime: Start time in YYYY-MM-DD HH:MM:SS format
        event_endtime: End time in YYYY-MM-DD HH:MM:SS format
        department: The department hosting the event
        description: A brief description of the event
        creator: Who ever uploaded the event. Ask the user their name, put anonymous if not willing. 
        confidence_scores: Confidence 0-100 per field, 
            example: {"event_title": 50, "event_location": 65}
        require_user_input: True if the user corrected any fields, creator does not count toward this metric 
            False if the AI extraction was accepted with out changes
        fields_edited: List of field names the user corrected,
            example: ["event_title", "department]. empty list if no edits.
    Returns:
        Confirmation message with created event ID
    """
    now = datetime.now()

    event = Event(
            time_created=now,
            event_title=event_title if event_title else None,
            event_location=event_location if event_location else None,
            event_startime=datetime.fromisoformat(event_startime) if event_startime else None,
            event_endtime=datetime.fromisoformat(event_endtime) if event_endtime else None,
            department=department if department else None,
            description=description if description else None,
            creator=creator 
            )

    event_id = create_event(event)

    flyer = Flyer(
        flyer_id=event_id + 8000000,
        upload_time=now,
        confidence_scores=confidence_scores,
        require_user_input=require_user_input,
        fields_edited=fields_edited,
        event_id=event_id
            )

    flyer_id = create_flyer(flyer)

    return f"Event *{event_title}* was created with Event ID: {event_id} and Flyer ID:{flyer_id}"
