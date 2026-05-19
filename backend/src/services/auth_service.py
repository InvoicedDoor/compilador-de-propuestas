from ..repos.auth_repo import (
    get_auth, 
    change_password, 
    get_user_by_mail, 
    register_user_repo)
from ..repos.user_repo import (
    get_users,
    get_user_by_id, 
    add_user_repo)
from src.utilities.hashing.hashing_password import (
    validate_password, 
    password_encryption)
from src.models.user_model import (
    RegisterUser, 
    User)
from src.models.auth_model import (
    RegisterCredentials, 
    Auth)
from src.utilities.handlers.http_exceptions import *
from src.utilities.db.db_connection import SessionLocal
from src.utilities.logger.logger import Logger
from config import Config
from flask import jsonify
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
            'rol': user.rol_id,
            'exp': datetime.utcnow() + timedelta(minutes=120)
        }

        return encode(payload, key, algorithm='HS256')

    except DomainError as domErr:
        raise domErr

    except Exception as ex:
        Logger.add_to_log('error', format_exc())
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
            return NotFound("El correo no está registrado.")
        
        is_valid = validate_password(old_password, credentials.password)

        if not is_valid:
            return BadRequest("No capturaste la contraseña correcta. No puedes cambiar la contraseña sin las credenciales correctas.")
        
        hashed_password = password_encryption(new_password)
        is_changed = change_password(session, mail, hashed_password)
        if not is_changed:
            return InternalServerError("No se pudo cambiar la contraseña.")
        
        return "Contraseña modificada con éxito."

    except DomainError as domErr:
        raise domErr

    except:
        Logger.add_to_log('error', format_exc())
        raise InternalServerError("Error en el servidor.")
    finally:
        session.close()


def register_user(user: RegisterUser, credentials: RegisterCredentials):
    session = SessionLocal()

    try:
        exist_user = get_user_by_mail(session, credentials.mail)

        if exist_user:
            raise Conflict("El usuario ya existe en la base de datos.")
        
        new_user = User(**user.model_dump())

        saved_user = add_user_repo(session, new_user)

        if not saved_user.id:
            session.rollback()

            raise InternalServerError("El usuario no se pudo registrar.")

        new_password  = password_encryption(
            credentials.password
        )

        new_user_credentials = Auth(
            user_id=saved_user.id,
            mail=credentials.mail,
            password=new_password
        )

        resp_credentials = register_user_repo(
            session,
            new_user_credentials
        )

        if not resp_credentials:
            session.rollback()

            raise BadRequest('No se pudo realizar el registro.')

        session.commit()

        return "Registro realizado."
    
    except DomainError as domErr:
        raise domErr

    except Exception:
        session.rollback()

        Logger.add_to_log(
            'error',
            format_exc()
        )

        raise InternalServerError("Error")

    finally:
        session.close()