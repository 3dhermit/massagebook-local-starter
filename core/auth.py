import bcrypt
from database.db import get_session
from database.models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def authenticate(username: str, password: str):
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(password, user.password_hash):
            return user
        return None
    finally:
        session.close()

def create_user(username: str, password: str, role: str = 'therapist'):
    session = get_session()
    try:
        if session.query(User).filter_by(username=username).first():
            return None  # User exists
        hashed = hash_password(password)
        user = User(username=username, password_hash=hashed, role=role)
        session.add(user)
        session.commit()
        return user
    finally:
        session.close()