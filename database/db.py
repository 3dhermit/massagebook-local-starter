import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base
from datetime import datetime
import shutil

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'massagebook.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    # Seed default data if empty
    session = SessionLocal()
    try:
        from .models import User, Service
        if not session.query(User).first():
            # Create default admin user (password: admin123 - change in production!)
            import bcrypt
            hashed = bcrypt.hashpw(b'admin123'.encode('utf-8'), bcrypt.gensalt())
            admin = User(username='admin', password_hash=hashed.decode('utf-8'), role='admin')
            session.add(admin)
        
        if not session.query(Service).first():
            default_services = [
                Service(name='Swedish Massage (60 min)', duration_minutes=60, price=120.0),
                Service(name='Deep Tissue (60 min)', duration_minutes=60, price=140.0),
                Service(name='Hot Stone (90 min)', duration_minutes=90, price=160.0),
            ]
            session.add_all(default_services)
        session.commit()
    finally:
        session.close()

def get_session():
    return SessionLocal()

def backup_database(backup_dir='backups'):
    """Create a timestamped backup of the database file."""
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'massagebook_backup_{timestamp}.db')
    shutil.copy2(DB_PATH, backup_path)
    return backup_path

def export_to_csv(session, model_class, output_path):
    """Generic CSV export for any model."""
    import pandas as pd
    query = session.query(model_class)
    df = pd.read_sql(query.statement, session.bind)
    df.to_csv(output_path, index=False)
    return output_path