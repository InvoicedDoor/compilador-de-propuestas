from src.repos.project_events.repo import verify_project_approbation
from src.repos.projects.repo import get_project_by_id
from src.repos.project_users.repo import verify_project_user
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.dtos.project_events.dto import ProjectEventDto
from src.utilities.db.db_connection import SessionLocal
from config import (
    ALTERNATIVE_STATUS, 
    APPROVAL_STEPS, 
    CLOSER_STATUS)

def update_project_status_service(project_changes: ProjectEventDto, status: str):
    session = SessionLocal()
    APPROVAL_PERSON = []
    try:
        # Validate owner
        is_valid = verify_project_user(session, project_changes.user_id, project_changes.project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        # Get project info
        project = get_project_by_id(session, project_changes.project_id)

        # Validate if project status wasn't cancelled, refused or finished
        if (project.status.status in CLOSER_STATUS):
            raise BadRequest("No se pueden actualizar los proyectos que se han terminado, cancelado o rechazado.")

        current_step = 0

        # Check the current project step
        if status not in ALTERNATIVE_STATUS:
            for step in range(len(APPROVAL_STEPS)):
                if APPROVAL_STEPS[f"STEP_{step + 1}"]["status"] == project.status.status:
                    current_step = step+1
                    APPROVAL_PERSON = APPROVAL_STEPS[f"STEP_{step + 1}"]["approver"]

            # Validate correct next step
            if status != APPROVAL_STEPS[f"STEP_{current_step + 1}"]["status"]:
                # Verificar que corresponda al siguiente paso del flujo
                raise BadRequest("No puedes actualizar a este estatus.") 

        # Validate approval desition.
        project_approbations = verify_project_approbation(session, project.id, project.status.status)

        for approbation in project_approbations:
            if approbation not in APPROVAL_PERSON:
                return  BadRequest("El proyecto no está autorizado para aprobarse.")
                
        # Update project status.

        return "Proyecto actualizado."

    except DomainError:
        raise

    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar la petición.") 
    
    finally:
        session.close()

def inactive_project_status_service(project_changes: ProjectEventDto, status: bool):
    session = SessionLocal()
    try:
        # Validate owner
        is_valid = verify_project_user(session, project_changes.user_id, project_changes.project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        # Get project info
        project = get_project_by_id(session, project_changes.project_id)

        # Validate if project status wasn't cancelled, refused or finished
        if (project.status.status in CLOSER_STATUS):
            raise BadRequest("No se pueden actualizar los proyectos que se han terminado, cancelado o rechazado.")

        current_step = 0

        # Check the current project step
        if status not in ALTERNATIVE_STATUS:
            for step in range(len(APPROVAL_STEPS)):
                if APPROVAL_STEPS[f"STEP_{step+1}"]["status"] == project.status.status:
                    current_step = step+1

            # Validate correct next step
            if status != APPROVAL_STEPS[f"STEP_{current_step + 1}"]["status"]:
                # Verificar que corresponda al siguiente paso del flujo
                raise BadRequest("No puedes actualizar a este estatus.") 

        # Validate approval desition.
        project_approbations = verify_project_approbation(session, project.id, status)

        # Update project status.        

        return "Proyecto actualizado."

    except DomainError:
        raise

    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 
    
    finally:
        session.close()