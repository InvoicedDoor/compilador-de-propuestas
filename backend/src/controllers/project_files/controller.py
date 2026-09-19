from src.services.project_files.service import (
    get_project_files_service,
    add_project_files_service,
    inactive_project_file_service)
from src.utilities.files_manager.validate_project_files import validate_project_files
from src.dtos.projects.dto import ProjectFilter
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_files.dto import DeleteProjectFileDto
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import (
    DomainError, 
    InternalServerError,
    BadRequest)
from src.utilities.handlers.http_success import (
    OK,
    Created)
from pydantic import ValidationError
from fastapi import APIRouter, Depends, Path, UploadFile, File, Body
import traceback

project_files_routes = APIRouter()

# Obtiene el listado de archivos cargados por proyecto
@project_files_routes.get('/{project_id}')
def get_project_files_controller(project_id: int = Path(...), user: RequesterUserDto = Depends(verify_authentication)):
    try:
        project = get_project_files_service(user, project_id=project_id)
        return OK("Datos encontrados.", project).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')

# Add files to specific project
@project_files_routes.post('/{project_id}')
def add_project_files_controller(project_id: int = Path(...),
                                 project_documentation: list[UploadFile] = File(...), 
                                 user: RequesterUserDto = Depends(verify_authentication)):
    try:
        errors = []
        files = []

        files = validate_project_files(
            project_documentation
        )
            
        service_message = add_project_files_service(user.id, project_id, files)

        return Created(message=service_message).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()

# # Update new project files
# @project_files_routes.patch('/{file_id}')
# @verify_authentication
# def update_project_files_controller(file_id: int = Path(...)):
#     try:
#         project: ProjectFilter = ProjectFilter()

#         return Created(message="").to_response()
    
#     except DomainError as domErr:
#         return domErr.to_dict()

#     except Exception:
#         Logger.add_to_system_log('error', traceback.format_exc())
#         return InternalServerError('Error').to_dict()

# Remove files from specific project
@project_files_routes.delete('/{project_id}')
def delete_project_files_controller(
    file_id: DeleteProjectFileDto = Body(...),
    project_id: int = Path(..., gt=0),
    requester: RequesterUserDto = Depends(verify_authentication)
):
    try:
        inactive_project_file_service(requester.id, project_id, file_id)

        Logger.add_to_events_log("info", f"Archivo {file_id} del proyecto {project_id} retirado por {requester.name} en la cuenta {requester.mail}.")

        return OK("Elemento eliminado.").to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except ValidationError as ve:
        count = 1
        response_string = "Campos incorrectos: "
        errors = ve.errors()
        for error in errors:
            field = error["loc"][0]
            message = error["msg"]
            if count < len(errors):
                response_string += f"{field} ({message}), "
                count += 1
            else: 
                count += 1
                response_string += f"{field} ({message})"

        return BadRequest(response_string).to_dict()

    except Exception as e:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError("Error").to_dict()