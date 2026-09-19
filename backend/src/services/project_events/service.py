from src.repos.projects.repo import get_project_by_id
from src.repos.project_users.repo import (
    verify_project_user, 
    validate_user_project_role, 
)
from src.repos.project_events.repo import (
    get_user_event_project,
    approve_project,
)
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_events.dto import (
    ApproveProjectDto,
    ProjectEventDto)
from src.utilities.db.db_connection import SessionLocal

def approve_project_service(requester: RequesterUserDto, body_approval: ApproveProjectDto, project_id: int):
    session = SessionLocal()
    try:
        requester_id = requester.id
        is_valid = verify_project_user(session, requester_id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        is_approver = validate_user_project_role(session, requester_id, project_id)

        if not is_approver:
            raise BadRequest("No tienes permisos para realizar esta acción.")

        project_status = get_project_by_id(session, project_id)

        new_event = ProjectEventDto(
            user_id=requester_id,
            project_id=project_id,
            status_code=project_status.status.status,
            approved=body_approval.approved
        )

        exist_event = get_user_event_project(session, new_event)

        if exist_event:
            raise Conflict("El estado ya fue aprobado/denegado por el usuario.")
        
        result = approve_project(session, new_event)

        if not result:
            session.rollback()
            raise UnprocessableEntity("No se aprobó la fase del proyecto.")
        session.commit()
        return f"Proyecto aprobado."
    
    except DomainError:
        raise 
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise InternalServerError("Error al aprobar el recurso. Consulte al administrador del sistema.") 
    
    finally:
        session.close()