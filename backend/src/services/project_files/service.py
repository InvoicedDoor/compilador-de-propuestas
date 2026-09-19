from src.repos.project_files.repo import (
    get_project_files,
    inactivate_project_file
)
from src.repos.project_users.repo import verify_project_user
from src.utilities.files_manager.upload_files_funtion import upload_files
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.dtos.users.dto import RequesterUserDto
from src.dtos.projects.dto import ImageMetadata
from src.utilities.db.db_connection import SessionLocal

def get_project_files_service(user: RequesterUserDto, project_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_project_user(session, user.id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        project_files = get_project_files(session, project_id)

        formated_project = [{
            "id": project_file.id,
            "filename": project_file.filename,
            "path": project_file.path
        } for project_file in project_files]

        return formated_project
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar la petición.") 
    finally:
        session.close()


def add_project_files_service(user_id: int, project_id: int, project_files: list, metadata: list[ImageMetadata]):
    session = SessionLocal()
    try:        
        results = []

        is_valid = verify_project_user(session, user_id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        results = upload_files(session, project_files, project_id)

        if any(r["status"] is True for r in results):
            session.commit()
            return "Subido correctamente."

        session.rollback()
        raise UnprocessableEntity("Error insertando uno o más archivos.")
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 
    
    finally:
        session.close()

def inactive_project_file_service(user_id: int, project_id: int, file_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_project_user(session, user_id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        result = inactivate_project_file(session, project_id, file_id)

        if not result:
            session.rollback()
            raise UnprocessableEntity("No se pudo eliminar el elemento.")

        session.commit()

        return "Elemento eliminado"

    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 

    finally:
        session.close()