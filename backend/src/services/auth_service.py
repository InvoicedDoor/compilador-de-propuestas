from ..repos.auth_repo import (
    get_auth, 
    change_password)
from ..repos.user_repo import (
    get_user_by_mail)
from src.utilities.hashing.hashing_password import (
    validate_password, 
    password_encryption)
from .users_service import (
    get_user_by_id_service
)
from src.utilities.handlers.http_exceptions import *
from src.utilities.db.db_connection import SessionLocal
from src.utilities.logger.logger import Logger
from config import Config
from traceback import format_exc
from jwt import encode
from datetime import (
    datetime, 
    timedelta)

key = Config.SECRET_KEY

def auth_service(mail: str, password: str):
    session = SessionLocal()
    try:
        credentials = get_auth(session, mail)

        if not credentials:
            raise NotFound("El usuario no existe.")

        valid_password = validate_password(password, credentials.password)

        if not valid_password:
            raise BadRequest("La contraseña es incorrecta.")
        
        user = credentials.user

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


def change_password_service(mail: str, old_password: str = None, new_password: str = None, new_password_confirmation: str = None):
    
    if new_password != new_password_confirmation:
        raise BadRequest("La contraseña no coincide con la confirmación.")
    
    session = SessionLocal()

    try:
        credentials = get_user_by_mail(session, mail)
        if not credentials:
            raise NotFound("El correo no está registrado.")
        
        is_valid = validate_password(old_password, credentials.password)

        if not is_valid:
            raise BadRequest("No capturaste la contraseña correcta. No puedes cambiar la contraseña sin las credenciales correctas.")
        
        hashed_password = password_encryption(new_password)
        is_changed = change_password(session, mail, hashed_password)
        if not is_changed:
            raise InternalServerError("No se pudo cambiar la contraseña.")
        
        return "Contraseña modificada con éxito."

    except DomainError:
        raise

    except:
        Logger.add_to_system_log('error', format_exc())
        raise InternalServerError("Error en el servidor.")
    finally:
        session.close()