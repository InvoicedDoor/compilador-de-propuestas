from config import Config
from src.dtos.auth.dto import ChangePasswordDto
from src.repos.credentials.repo import change_password
from src.repos.users.repo import get_user_by_mail
from src.utilities.db.db_connection import SessionLocal
from src.utilities.handlers.http_exceptions import *
from src.utilities.hashing.hashing_password import (
    validate_password, 
    password_encryption)
from src.utilities.logger.logger import Logger
from traceback import format_exc

key = Config.SECRET_KEY

def change_password_service(updated_credentials: ChangePasswordDto):
    mail = updated_credentials.mail
    old_password = updated_credentials.old_password
    new_password = updated_credentials.new_password
    new_password_confirmation = updated_credentials.new_password_confirmation
    
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