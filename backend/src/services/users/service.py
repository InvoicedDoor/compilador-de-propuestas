from src.repos.users.repo import (
    get_users,
    get_user_by_id,
    get_user_by_mail,
    validate_user,
    register_user_repo
)
from src.utilities.hashing.hashing_password import (
    password_encryption)
from src.models.users.model import (
    UserModel)
from src.dtos.users.dto import UserDto
from src.models.credentials.model import (
    Auth)
from src.dtos.credentials.dto import (
    CredentialDto
)
from src.dtos.users.dto import RequesterUserDto, UserFilterDto, UserDto
from src.utilities.handlers.http_exceptions import *
from src.utilities.db.db_connection import SessionLocal
from src.utilities.logger.logger import Logger
from traceback import format_exc

def get_users_service(user: UserFilterDto, user_requester: RequesterUserDto):
    session = SessionLocal()
    try:
        users_format = []
        if not validate_user(user_requester):
            user.rol_id = 2
            user.active = 1

        list_data = get_users(user)

        for data in list_data:
            users_format.append({
                "id": data.id,
                "name": data.name,
                "first_lastname": data.first_lastname,
                "second_lastname": data.second_lastname,
                "rol": {
                    "id": data.rol.id,
                    "rol": data.rol.rol
                }
            })

        return users_format
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()

def get_user_by_id_service(user_id: int):
    session = SessionLocal()
    try:
        repo_res = get_user_by_id(session, user_id)

        if not repo_res:
            raise InternalServerError("Error al obtener los datos de usuario. Informar a soporte.")
        json_format = {
            "name": repo_res.name,
            "rol": repo_res.role.rol
        }
        return json_format
    except Exception as ex:
        return {}
    finally:
        session.close()

def register_user(user: UserDto, credentials: CredentialDto):
    session = SessionLocal()

    try:
        exist_user = get_user_by_mail(session, credentials.mail)

        if exist_user:
            raise Conflict("El usuario ya existe en la base de datos.")
        
        new_user = UserModel(**user.model_dump())

        saved_user = register_user_repo(session, new_user)

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
    
    except DomainError:
        raise

    except Exception:
        session.rollback()

        Logger.add_to_system_log(
            'error',
            format_exc()
        )

        raise InternalServerError("Error")

    finally:
        session.close()