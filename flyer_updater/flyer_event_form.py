import streamlit as st
from datetime import datetime  
from event_module.event import Event
from event_module.event_fetcher import create_event
from flyer_updater.flyer import Flyer
from flyer_updater.flyer_fetcher import create_flyer


LOW_CONFIDENCE_THRESHOLD = 70


def _label(base_label, field_key, scores):
    """Append a warning icon + score to the label if confidence is low."""
    score = scores.get(field_key, 0)
    if score and score < LOW_CONFIDENCE_THRESHOLD:
        return f"{base_label} ⚠️ ({score}%)"
    return base_label


def _parse_iso(iso_str):
    """Parse an ISO datetime string into (date, time). Falls back to now if invalid."""
    if not iso_str:
        now = datetime.now()
        return now.date(), now.time().replace(microsecond=0)
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.date(), dt.time()
    except ValueError:
        now = datetime.now()
        return now.date(), now.time().replace(microsecond=0)


def render_event_form():
    """Open the event form as a modal dialog when pending_event is set."""
    if not st.session_state.pending_event:
        return
    _event_form_dialog()


@st.dialog("Review Event Details")
def _event_form_dialog():
    pending = st.session_state.pending_event
    if not pending:
            return 
    scores = pending.get("confidence_scores", {})

    st.caption("Fields marked ⚠️ had lower extraction confidence — please verify.")

    start_date, start_time = _parse_iso(pending.get("event_startime", ""))
    end_date, end_time = _parse_iso(pending.get("event_endtime", ""))

    with st.form("event_form_{st.session_state.event_form_key}"):
        title = st.text_input(
            _label("Event Title", "event_title", scores),
            value=pending.get("event_title", ""),
        )
        location = st.text_input(
            _label("Location", "event_location", scores),
            value=pending.get("event_location", ""),
        )

        st.markdown(_label("**Start**", "event_startime", scores))
        col_sd, col_st = st.columns(2)
        with col_sd:
            start_date_input = st.date_input(
                "Date", value=start_date, key="start_date", label_visibility="collapsed"
            )
        with col_st:
            start_time_input = st.time_input(
                "Time", value=start_time, key="start_time", label_visibility="collapsed"
            )

        st.markdown(_label("**End**", "event_endtime", scores))
        col_ed, col_et = st.columns(2)
        with col_ed:
            end_date_input = st.date_input(
                "Date", value=end_date, key="end_date", label_visibility="collapsed"
            )
        with col_et:
            end_time_input = st.time_input(
                "Time", value=end_time, key="end_time", label_visibility="collapsed"
            )

        dept = st.text_input(
            _label("Department", "department", scores),
            value=pending.get("department", ""),
        )
        desc = st.text_area(
            _label("Description", "description", scores),
            value=pending.get("description", ""),
            height=80,
        )
        creator = st.text_input("Your name", value=pending.get("creator", ""))

        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("Submit to Calendar", type="primary")
        with col_cancel:
            cancelled = st.form_submit_button("Cancel")

    if submitted:
        edited = {
            "event_title": title,
            "event_location": location,
            "event_startime": datetime.combine(start_date_input, start_time_input).isoformat(sep=" "),
            "event_endtime": datetime.combine(end_date_input, end_time_input).isoformat(sep=" "),
            "department": dept,
            "description": desc,
            "creator": creator,
            "confidence_scores": scores,
        }
        _handle_event_submit(edited)

    if cancelled:
        st.session_state.pending_event = None
        st.session_state.original_extraction = None
        st.session_state.event_form_key +=1
        st.rerun()


def _handle_event_submit(edited):
    """Diff edits, insert event and flyer, clear state."""
    original = st.session_state.original_extraction or {}
    tracked_fields = [
        "event_title", "event_location", "event_startime",
        "event_endtime", "department", "description",
    ]
    fields_edited = [
        f for f in tracked_fields
        if edited.get(f) != original.get(f)
    ]
    require_user_input = len(fields_edited) > 0

    try:
        now = datetime.now()
        event = Event(
            time_created=now,
            event_title=edited["event_title"] or None,
            event_location=edited["event_location"] or None,
            event_startime=datetime.fromisoformat(edited["event_startime"]) if edited["event_startime"] else None,
            event_endtime=datetime.fromisoformat(edited["event_endtime"]) if edited["event_endtime"] else None,
            department=edited["department"] or None,
            description=edited["description"] or None,
            creator=edited["creator"],
        )
        event_id = create_event(event)

        flyer = Flyer(
            flyer_id=event_id + 8000000,
            upload_time=now,
            confidence_scores=edited["confidence_scores"],
            require_user_input=require_user_input,
            fields_edited=fields_edited,
            event_id=event_id,
        )
        create_flyer(flyer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Event **{edited['event_title']}** was saved to the calendar!",
        })
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Something went wrong saving the event: {e}",
        })

    st.session_state.pending_event = None
    st.session_state.original_extraction = None
    st.session_state.event_form_key +=1
    st.rerun()
