from src.services.project_status.service import update_project_status_service
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_status.dto import UpdateProjectStatusBody
from src.dtos.project_events.dto import ProjectEventDto
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import (
    DomainError, 
    InternalServerError)
from src.utilities.handlers.http_success import Created
from fastapi import APIRouter, Depends, Path, Body
import traceback

project_status_routes = APIRouter()

# Update project status (active or inactive)
@project_status_routes.patch('{project_id}')
def update_project_status_controller(
    project_id: int = Path(..., gt=0),
    json_data: UpdateProjectStatusBody = Body(...),
    requester: RequesterUserDto = Depends(verify_authentication)):
    try:
        project_changes: ProjectEventDto = ProjectEventDto(
            user_id=requester.id,
            project_id=project_id
        )

        res = update_project_status_service(project_changes,json_data.status)

        return Created(message=res).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()