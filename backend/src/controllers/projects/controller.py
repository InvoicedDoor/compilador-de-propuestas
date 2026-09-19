from src.services.projects.service import (
    add_project_service, 
    get_projects_service, 
    get_project_by_id_service)
from src.utilities.files_manager.validate_project_files import validate_project_files
from src.dtos.projects.dto import (
    ProjectDto, 
    ProjectFilter)
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_status.dto import UpdateProjectStatusBody
from src.dtos.project_users.dto import DeleteProjectUsersBody
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import (
    DomainError, 
    InternalServerError)
from src.utilities.handlers.http_success import (
    OK,
    Created)
from fastapi import Request, APIRouter, Depends, Path, Form, UploadFile, File
import traceback

projects_routes = APIRouter()

# Obtiene el listado de proyectos
@projects_routes.get('')
def get_all_project_controller(user: RequesterUserDto = Depends(verify_authentication)):
    try:
        project: ProjectFilter = ProjectFilter()

        data = get_projects_service(user, project)

        return OK("Datos encontrados.", data).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()

# Obtiene un proyecto por Id
@projects_routes.get('/{project_id}')
def get_project_by_id_controller(request: Request, project_id: int = Path(..., gt=0), user: RequesterUserDto = Depends(verify_authentication)):
    try:
        project = get_project_by_id_service(user, project_id=project_id)
        return OK("Datos encontrados.", project).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')

# Carga un nuevo proyecto
@projects_routes.post("")
async def send_projects_controller(
    project_title: str = Form(...),
    project_description: str = Form(...),
    project_documentation: list[UploadFile] = File(...),
    user: RequesterUserDto = Depends(verify_authentication),
):
    try:
        user_id = user.id
        files = validate_project_files(
            project_documentation
        )

        project = ProjectDto(
            project_title=project_title,
            project_description=project_description,
            project_manager=user_id
        )

        service_message = await add_project_service(
            user_id,
            project,
            files
        )

        Logger.add_to_events_log("info", f"El usuario {user.mail} creó el proyecto {project_title}.")

        return Created(
            message=service_message
        ).to_response()
    
    except DomainError as dexc:
        Logger.add_to_events_log("error", dexc.message)
        return dexc.to_dict()

    except Exception as ex:
        Logger.add_to_system_log("critical", ex)
        return InternalServerError("Error en el servidor.")