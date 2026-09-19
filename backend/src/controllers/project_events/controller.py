from src.services.project_events.service import approve_project_service
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_events.dto import ApproveProjectDto
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import (
    DomainError, 
    InternalServerError)
from src.utilities.handlers.http_success import (
    OK)
from fastapi import APIRouter, Depends, Path, Body
import traceback

project_events_routes = APIRouter()

# Approve project status
@project_events_routes.post('/{project_id}/approve')
def approve_project_controller(
    project_id: int = Path(..., gt=0),
    body_request: ApproveProjectDto = Body(...),
    requester: RequesterUserDto = Depends(verify_authentication)):
    try:
        approve_project_service(requester, body_request, project_id)

        return OK("Proyecto aprobado.").to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()