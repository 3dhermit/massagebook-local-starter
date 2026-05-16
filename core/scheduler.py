from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import Appointment

def check_availability(session: Session, start_time: datetime, end_time: datetime, exclude_id: int = None) -> bool:
    """Check if the time slot is available (no overlapping appointments)."""
    query = session.query(Appointment).filter(
        Appointment.status.in_(['scheduled', 'confirmed']),
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    )
    if exclude_id:
        query = query.filter(Appointment.id != exclude_id)
    return query.count() == 0

def get_available_slots(session: Session, date: datetime, duration_minutes: int = 60, business_hours=(9, 18)):
    """Simple slot generator for a given day (demo purposes)."""
    slots = []
    start_hour, end_hour = business_hours
    current = datetime.combine(date.date(), datetime.min.time().replace(hour=start_hour))
    end_of_day = datetime.combine(date.date(), datetime.min.time().replace(hour=end_hour))
    
    while current + timedelta(minutes=duration_minutes) <= end_of_day:
        end = current + timedelta(minutes=duration_minutes)
        if check_availability(session, current, end):
            slots.append((current, end))
        current += timedelta(minutes=30)  # 30-min increments
    return slots

def book_appointment(session: Session, client_id: int, service_id: int, start_time: datetime, end_time: datetime, notes: str = ""):
    """Book a new appointment with conflict check."""
    if not check_availability(session, start_time, end_time):
        raise ValueError("Time slot is not available.")
    
    appt = Appointment(
        client_id=client_id,
        service_id=service_id,
        start_time=start_time,
        end_time=end_time,
        notes=notes,
        status='scheduled'
    )
    session.add(appt)
    session.commit()
    return appt