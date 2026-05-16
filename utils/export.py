import os
from datetime import datetime
from database.db import backup_database, get_session, export_to_csv
from database.models import Client, Appointment

def perform_backup():
    """Perform database backup and return path."""
    backup_path = backup_database()
    return backup_path

def export_clients_csv(output_dir='exports'):
    os.makedirs(output_dir, exist_ok=True)
    session = get_session()
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(output_dir, f'clients_{timestamp}.csv')
        return export_to_csv(session, Client, path)
    finally:
        session.close()

def export_appointments_csv(output_dir='exports'):
    os.makedirs(output_dir, exist_ok=True)
    session = get_session()
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(output_dir, f'appointments_{timestamp}.csv')
        return export_to_csv(session, Appointment, path)
    finally:
        session.close()