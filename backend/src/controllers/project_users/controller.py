from src.services.project_users.service import (
    get_project_users_service,
    add_project_user_service,
    update_project_user_service,
    inactive_project_user_service)
from src.dtos.project_users.dto import ( 
    ProjectUsersFilter,
    UpdateProjectUserRoleDto,
    AddProjectUserRequestBody,
    DeleteProjectUsersDto)
from src.dtos.users.dto import RequesterUserDto
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import (
    DomainError, 
    BadRequest,
    InternalServerError)
from src.utilities.handlers.http_success import (
    OK,
    Created,
    NoContent)
from fastapi import APIRouter, Depends, Path, Body
import traceback

project_users_routes = APIRouter()

# Obtiene el listado de usuarios por proyecto
@project_users_routes.get('/{project_id}')
def get_project_users_controller(
    project_id: int = Path(..., gt=0),
    user: RequesterUserDto = Depends(verify_authentication)):
    try:
        project = get_project_users_service(user, ProjectUsersFilter(project_id=project_id, active=1))
        return OK("Datos encontrados.", project).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')

# Add new user to project
@project_users_routes.post('/{project_id}')
def add_project_users_controller(
    project_id: int = Path(..., gt=0),
    users_list: AddProjectUserRequestBody = Body(...),
    requester: RequesterUserDto = Depends(verify_authentication)):
    try:
        res = add_project_user_service(users_list.users, requester.id, project_id)

        return Created(res).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()

# Update project users
@project_users_routes.patch('/{project_id}')
def update_project_users_controller(
    user_update: UpdateProjectUserRoleDto = Body(...),
    project_id: int = Path(..., gt=0),
    requester: RequesterUserDto = Depends(verify_authentication)):
    try:
        res = update_project_user_service(user_update, requester.id, project_id)

        return Created(res).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()

# Remove project users
@project_users_routes.delete('/{project_id}')
def inactive_project_users_controller(
    users_list: DeleteProjectUsersDto = Body(...),
    project_id: int = Path(..., gt=0),
    requester: RequesterUserDto = Depends(verify_authentication)):
    try:
        inactive_project_user_service(requester, project_id, users_list)

        return NoContent("Operación completada.").to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except BadRequest as br:
        Logger.add_to_system_log("error", br.to_log_format())
        return InternalServerError("Error al remover los usuarios del proyecto.").to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError("Error al inactivar al usuario.").to_dict()