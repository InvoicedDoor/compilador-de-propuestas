from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.credentials.model import Auth
from src.utilities.logger.logger import Logger
import traceback

def get_auth(session: Session,mail: str):
    try:
        query = select(Auth).where(
            Auth.mail == mail
        )

        result = session.execute(query)

        return result.unique().scalar_one_or_none()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al autenticarse.")