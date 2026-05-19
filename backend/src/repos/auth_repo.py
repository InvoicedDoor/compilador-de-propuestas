from src.utilities.db.db_connection import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import joinedload, Session
from src.models.user_model import User, RegisterUser
from src.models.auth_model import Auth, RegisterCredentials
from src.utilities.logger.logger import Logger
import traceback

def get_hashed_password(session: Session, mail: str):
    try:
        query = (select(Auth)
        .options(
            joinedload(Auth.user)
        )
        .where(
            Auth.mail == mail
        ))

        result = session.execute(query)

        credentials = result.scalar_one_or_none()

        return credentials
    except:
        Logger.add_to_log("error", traceback.format_exc())

        raise ValueError(
            "Error al obtener la autenticación."
        )


def get_auth(session: Session,mail: str):
    try:
        query = select(Auth).where(
            Auth.mail == mail
        )

        result = session.execute(query)

        return result.unique().scalar_one_or_none()
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al autenticarse.")
    

def change_password(session: Session, mail: str, new_password: str):
    try:

        user = session.query(Auth)\
            .filter(
                Auth.mail == mail
            ).first()

        if not user:
            return False

        user.password = new_password

        session.commit()

        return True

    except Exception as ex:

        session.rollback()

        Logger.add_to_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(f"Error: {ex}")

    finally:

        session.close()
    
def get_user_by_mail(session: Session, mail: str):
    try:

        query = select(Auth).where(
            Auth.mail == mail
        )

        result = session.execute(query)

        credentials = result.unique().scalar_one_or_none()

        if not credentials:
            return None

        return credentials

    except Exception as ex:

        Logger.add_to_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(f"Error: {ex}")
    
def register_user_repo(
    session: Session,
    credentials: Auth
):

    try:
        session.add(credentials)

        session.flush()

        return True

    except Exception:

        session.rollback()

        Logger.add_to_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(
            "Error al agregar usuario."
        )