from .service import get_projects_service, get_project_by_id_service, add_project_service, update_project_status_service
from .dto import *
from ..models.user_model import RequesterUser
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from json import loads
from config import Config
from werkzeug.exceptions import BadRequest as BdRq
from flask import Blueprint, request
import traceback

main = Blueprint('project_blueprint', __name__)

key = Config.SECRET_KEY
MAX_SIZE = 5 * 1024 * 1024

@main.get('')
@verify_authentication
def get_all_project_controller():
    try:
        project: GetProject = GetProject()

        data = get_projects_service(RequesterUser(**request.user), project)

        return OK("Datos encontrados.", data).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except BdRq:
        return InternalServerError("Cuerpo de la petición mal formado.").to_dict()
    
    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')


@main.get('/<int:id>')
@verify_authentication
def get_project_by_id_controller(id: int):
    try:
        project = get_project_by_id_service(RequesterUser(**request.user), project_id=id)
        return OK("Datos encontrados.", project).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except BdRq:
        return InternalServerError("Cuerpo de la petición mal formado.").to_dict()
    
    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')


@main.post('')
@verify_authentication
def send_projects_controller():
    metadata_count = 0
    metadata = []
    try:
        data = request.form.to_dict()

        json_data = AddProject.model_validate(data)

        documentation = request.files.getlist("project_documentation")

        errors = []
        files = []

        if documentation:
            for file in documentation:
                if not file or not metadata[metadata_count]:
                    continue

                file.seek(0, 2)
                size = file.tell()
                file.seek(0)

                if size > MAX_SIZE:
                    raise BadRequest(f"{file.filename} demasiado grande.")

                files.append(file)

                metadata_count += 1

            if errors:
                raise BadRequest(errors)

        service_message = add_project_service(request.user["id"], json_data, files, metadata)

        return Created(message=service_message).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except BdRq:
        return InternalServerError("Cuerpo de la petición mal formado.").to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')


# @main.patch('/project-status/<int:id>')
# @verify_authentication
# def update_project_status_controller(id):
#     try:
#         requester_user = RequesterUser(**request.user)
#         json_data = UpdateProjectStatusBody.model_validate(request.get_json())

#         project_changes: ProjectEventDto = ProjectEventDto(
#             user_id=requester_user.id,
#             project_id=id
#         )

#         res = update_project_status_service(project_changes,json_data.status)

#         return Created(message=res).to_response()
    
#     except DomainError as domErr:
#         return domErr.to_dict()

#     except BdRq:
#         return InternalServerError("Cuerpo de la petición mal formado.").to_dict()

#     except Exception:
#         Logger.add_to_system_log('error', traceback.format_exc())
#         return InternalServerError('Error').to_dict()


# @main.delete("")
# @verify_authentication
# def inactive_project_controller(id):
#     try:
#         requester_user = RequesterUser(**request.user)
#         json_data = UpdateProjectStatusBody.model_validate(request.get_json())

        
#         return NoContent("").to_response()
    
#     except DomainError as domErr:
#         return domErr.to_dict()

#     except BdRq:
#         return InternalServerError("Cuerpo de la petición mal formado.").to_dict()
    
#     except Exception:
#         Logger.add_to_system_log('error', traceback.format_exc())
#         return InternalServerError('Error').to_dict()