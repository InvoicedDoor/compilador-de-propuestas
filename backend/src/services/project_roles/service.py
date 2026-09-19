from src.repos.project_roles.repo import get_all_roles
from src.dtos.project_roles.dto import ProjectRoleDto
from src.utilities.db.db_connection import SessionLocal
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from traceback import format_exc

def get_project_roles_service(filters: ProjectRoleDto):
    session = SessionLocal()
    try:
        project_roles = get_all_roles(session, filters)

        if len(project_roles) < 1:
            raise NotFound("No hay contenido.", [])

        formated_project_roles = [{
            "code": project_role.code,
            "description": project_role.description
        } for project_role in project_roles]

        return formated_project_roles
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("critical", format_exc())
        raise InternalServerError("Error en el sistema. Informe al administrador.")
    finally:
        session.close()