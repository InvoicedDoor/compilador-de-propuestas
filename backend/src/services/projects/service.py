from src.repos.projects.repo import (
    send_project, 
    get_all_project, 
    get_project_by_id, 
    )
from src.repos.project_users.repo import (
    verify_project_user, 
    get_all_user_project, 
    add_relation_user_project,
)
from src.repos.project_events.repo import get_status_events
from src.repos.users.repo import validate_user
from src.utilities.files_manager.upload_files_funtion import upload_files
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.dtos.users.dto import RequesterUserDto
from src.dtos.projects.dto import (
    ProjectDto, 
    ProjectFilter)
from src.dtos.project_events.dto import ProjectEventStatusDto
from src.utilities.db.db_connection import SessionLocal
from config import APPROVAL_STEPS, ROLE_APPROVER_PROJECT

def get_projects_service(user: RequesterUserDto, project: ProjectFilter):
    session = SessionLocal()
    try:
        project_format = []
        if validate_user(user):
            project_list = get_all_project(session, project)
        else:
            project_list = get_all_user_project(session, user.id, project)

        if len(project_list) == 0:
            raise NotFound(message="No hay propuestas aún.", data=[])

        for data in project_list:
            files = [{
                "filename": file.filename,
                "source": file.path
            } for file in data.project_files]

            project_format.append({
                "id": data.id,
                "title": data.title,
                "description": data.description,
                "status": {
                    "code": data.status.status,
                    "description": data.status.description
                },
                "source": files
            })
        return project_format
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()

def get_project_by_id_service(user: RequesterUserDto, project_id: int):
    session = SessionLocal()
    company_roles_needed = []
    try:
        is_valid = verify_project_user(session, user.id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        project = get_project_by_id(session, project_id)

        for step in APPROVAL_STEPS:
            if APPROVAL_STEPS[step]["status"] == project.status.status:
                company_roles_needed = APPROVAL_STEPS[step]["approver"]
                break

        if len(company_roles_needed) == 0:
            raise InternalServerError("Hubo un problema al obtener los roles.")

        filter_events_status = ProjectEventStatusDto(
            project_id=project_id,
            status_code=project.status.status,
            approver_roles=company_roles_needed,
            project_role_status_code=ROLE_APPROVER_PROJECT
        )

        project_events = get_status_events(session, filter_events_status)

        formated_project = {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "project_events": [{
                "name": event.name,
                "first_lastname": event.first_lastname,
                "second_lastname": event.second_lastname,
                "role": {
                    "code": event.code,
                    "role": event.rol
                },
                "approved": event.approved
            } for event in project_events],
            "active": project.active,
            "files": [
            {
                "id": file.id,
                "filename": file.filename,
                "path": file.path
            } for file in project.project_files]
        }

        return formated_project
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()

async def add_project_service(user_id: int, project: ProjectDto, project_files):
    session = SessionLocal()
    try:
        projectModel: ProjectFilter = ProjectFilter(title=project.project_title,description=project.project_description,)

        exist_project = get_all_project(session, projectModel)

        if exist_project:
            Logger.add_to_events_log("info", f"El proyecto {project.project_title} usuario {user_id}, falló.")
            raise Conflict("La propuesta ya existe.")

        project_id = send_project(session, project.project_title, project.project_description)

        if not project_id:
            Logger.add_to_events_log("info", f"El proyecto {project.project_title} del usuario {user_id}, falló.")
            raise InternalServerError("No se pudo crear la propuesta.")

        relation_ok = add_relation_user_project(session, user_id, project_id, project_role_id = 1)

        if not relation_ok:
            Logger.add_to_events_log("info", f"El proyecto {project.project_title} del usuario {user_id}, falló.")
            raise InternalServerError("No se pudo crear la relación usuario-propuesta.")
        
        if not project_files:
            session.commit()
            return "Propuesta vacía creada exitosamente."

        results = await upload_files(session, project_files, project_id)
        
        if any(r is False for r in results):
            session.rollback()
            Logger.add_to_events_log("info", f"El proyecto {project.project_title} del usuario {user_id}, falló.")
            raise InternalServerError("Error insertando uno o más archivos.")
        
        session.commit()
        return "Subido correctamente."
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 
    
    finally:
        session.close()