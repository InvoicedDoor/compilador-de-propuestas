from sqlalchemy import select
from sqlalchemy.orm import Session
from src.utilities.db.db_connection import SessionLocal
from src.models.user_model import RowUser, User
from src.models.auth_model import Auth
from src.utilities.logger.logger import Logger
import traceback

def get_users():
    session = SessionLocal()
    try:
        query = select(User)

        result = session.execute(query)

        users = result.scalars()

        return users.all()
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")

def get_user_by_id(user_id: int):
    session = SessionLocal()
    try:
        query = select(User).where(
            User.id == user_id
        )
        
        result = session.execute(query)

        return result.scalar_one_or_none()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")
    

def add_user_repo(session: Session, user: User):
    try:
        session.add(user)

        session.flush()

        return user

    except Exception as ex:
        session.rollback()
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al agregar al usuario.")