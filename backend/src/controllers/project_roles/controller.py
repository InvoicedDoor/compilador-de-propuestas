from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.dtos.project_roles.dto import ProjectRoleDto
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from src.services.project_roles.service import get_project_roles_service
from fastapi import APIRouter, Depends, Query
from src.utilities.logger.logger import Logger
import traceback

project_roles_routes = APIRouter()

@project_roles_routes.get('')
def get_all_project_roles_route(
    filters: ProjectRoleDto = Query(None),
    _: None = Depends(verify_authentication)
):
    try:
        project_roles = get_project_roles_service(filters)

        return OK("Datos encontrados.", project_roles).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()
