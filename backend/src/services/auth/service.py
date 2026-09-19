from src.dtos.auth.dto import AuthDto
from src.repos.credentials.repo import get_auth
from src.services.users.service import get_user_by_id_service
from src.utilities.hashing.hashing_password import validate_password
from src.utilities.handlers.http_exceptions import *
from src.utilities.db.db_connection import SessionLocal
from src.utilities.logger.logger import Logger
from config import Config
from datetime import (
    datetime, 
    timedelta)
from jwt import encode
from traceback import format_exc

key = Config.SECRET_KEY

def auth_service(credentials: AuthDto):
    session = SessionLocal()
    try:
        current_credentials = get_auth(session, credentials.mail)

        if not credentials:
            raise NotFound("El usuario no existe.")

        valid_password = validate_password(credentials.password, current_credentials.password)

        if not valid_password:
            raise BadRequest("La contraseña es incorrecta.")
        
        user = current_credentials.user

        if not user:
            raise NotFound("El usuario no tiene registro.")

        payload = {
            'id': user.id,
            'name': user.name,
            'mail': credentials.mail,
            'rol': user.company_role_id,
            'exp': datetime.utcnow() + timedelta(minutes=120)
        }

        user_info = get_user_by_id_service(user.id)

        return encode(payload, key, algorithm='HS256'), user_info

    except DomainError:
        raise

    except Exception as ex:
        Logger.add_to_system_log('error', format_exc())
        raise InternalServerError("Error.")
    finally:
        session.close()


def unauthorize_token_service(token: str):
    session = SessionLocal()
    try:
        pass
    except DomainError:
        raise

    except Exception as ex:
        Logger.add_to_system_log('error', format_exc())
        raise InternalServerError("Error.")
    finally:
        session.close()