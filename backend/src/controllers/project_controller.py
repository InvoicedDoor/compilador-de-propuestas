from ..services.project_service import (
    add_project_service, 
    get_projects_service, 
    get_project_by_id_service, 
    add_project_files_service, 
    get_project_users_service, 
    get_project_files_service, 
    update_project_status_service,
    update_project_user_service, 
    add_project_user_service,
    approve_project_service,
    inactive_project_file_service, 
    inactive_project_user_service)
from src.dtos.projects.dto import (
    ProjectDto, 
    ProjectFilter, 
    )
from src.dtos.project_files.dto import DeleteProjectFileDto
from src.dtos.project_events.dto import (
    ApproveProjectDto,
    ProjectEventDto)
from src.dtos.project_users.dto import (
    ProjectUserDto, 
    ProjectUsersFilter)
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_status.dto import UpdateProjectStatusBody
from src.dtos.project_users.dto import DeleteProjectUsersBody, UpdateProjectUserBody
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import (
    DomainError, 
    InternalServerError,
    BadRequest)
from src.utilities.handlers.http_success import (
    OK,
    Created,
    NoContent)
from json import loads
from config import Config
from werkzeug.exceptions import BadRequest as BdRq
from pydantic import ValidationError
from flask import Blueprint, request
import traceback

main = Blueprint('project_blueprint', __name__)

key = Config.SECRET_KEY
MAX_SIZE = 5 * 1024 * 1024

# Obtiene el listado de proyectos
@main.get('')
@verify_authentication
def get_all_project_controller():
    try:
        project: ProjectFilter = ProjectFilter()

        data = get_projects_service(RequesterUserDto(**request.user), project)

        return OK("Datos encontrados.", data).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')
    

# Obtiene el listado de usuarios por proyecto
@main.get('/project-users/<int:id>')
@verify_authentication
def get_project_users_controller(id: int):
    try:
        project = get_project_users_service(RequesterUserDto(**request.user), ProjectUsersFilter(project_id=id, active=1))
        return OK("Datos encontrados.", project).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')
    

# Obtiene el listado de archivos cargados por proyecto
@main.get('/project-files/<int:id>')
@verify_authentication
def get_project_files_controller(id: int):
    try:
        project = get_project_files_service(RequesterUserDto(**request.user), project_id=id)
        return OK("Datos encontrados.", project).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')
    


# Obtiene un proyecto por Id
@main.get('/<int:id>')
@verify_authentication
def get_project_by_id_controller(id: int):
    try:
        project = get_project_by_id_service(RequesterUserDto(**request.user), project_id=id)
        return OK("Datos encontrados.", project).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')


# Carga un nuevo proyecto
@main.post('')
@verify_authentication
def send_projects_controller():
    metadata_count = 0
    metadata = []
    try:
        data = request.form

        metadata_raw = request.form.get("metadata")
        documentation = request.files.getlist("project_documentation")

        if not data.get('project_title'): 
            raise BadRequest("El titulo no debe estar vacío.")

        errors = []
        files = []

        if metadata_raw and documentation:
            metadata = loads(metadata_raw)

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
            
        project = ProjectDto(project_title=data["project_title"],
        project_description=data["project_description"],
        project_manager=request.user["id"])

        service_message = add_project_service(request.user["id"], project, files, metadata)

        return Created(message=service_message).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error')
    

# Add files to specific project
@main.post('/<int:id>')
@verify_authentication
def add_project_files_controller(id):
    metadata_count = 0
    metadata = []
    try:
        documentation = request.files.getlist("project_documentation")

        errors = []
        files = []

        if documentation:
            for file in documentation:
                if not file:
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
            
        service_message = add_project_files_service(request.user["id"], id, files, metadata)

        return Created(message=service_message).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()


# Approve project status
@main.post('/<int:project_id>/approve')
@verify_authentication
def approve_project_controller(project_id):
    try:
        requester = RequesterUserDto(**request.user)
        body_request = ApproveProjectDto.model_validate(request.get_json())
        """
        {
            approved: <true | false>
        }
        """
        approve_project_service(requester, body_request, project_id)

        return OK("Proyecto aprobado.").to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()


# Add new user to project
@main.post('/project-users/<int:id>')
@verify_authentication
def add_project_users_controller(id: int):
    try:
        user_requester = RequesterUserDto(**request.user)
        users_list: list[ProjectUserDto] = request.json["users"]

        res = add_project_user_service(users_list, user_requester.id, id)

        return Created(res).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()


# Update new project files
@main.patch('/<int:id>')
@verify_authentication
def update_project_files_controller(id):
    try:
        project: ProjectFilter = ProjectFilter()

        return Created(message="").to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()


# Update project status (active or inactive)
@main.patch('/project-status/<int:id>')
@verify_authentication
def update_project_status_controller(id):
    try:
        requester_user = RequesterUserDto(**request.user)
        json_data = UpdateProjectStatusBody.model_validate(request.get_json())

        project_changes: ProjectEventDto = ProjectEventDto(
            user_id=requester_user.id,
            project_id=id
        )

        res = update_project_status_service(project_changes,json_data.status)

        return Created(message=res).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()


# Update project users
@main.patch('/project-users/<int:id>')
@verify_authentication
def update_project_users_controller(id: int):
    try:
        user_requester = RequesterUserDto(**request.user)
        users_list = UpdateProjectUserBody.model_validate(request.get_json())

        res = update_project_user_service(users_list, user_requester.id, id)

        return Created(res).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()


# Remove project users
@main.delete('/project-users/<int:id>')
@verify_authentication
def inactive_project_users_controller(id: int):
    try:
        to_inactive_ids = None

        if "user_id" in request.args:
            to_inactive_ids = [request.args.get("user_id", type=int)]

        else:
            users_list = DeleteProjectUsersBody.model_validate(request.get_json())
            to_inactive_ids = [user.user_id for user in users_list.users]

        user_requester = RequesterUserDto(**request.user)

        inactive_project_user_service(user_requester, id, to_inactive_ids)

        return NoContent("Operación completada.").to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except BdRq as br:
        Logger.add_to_system_log("error", br)
        return InternalServerError("Error al remover los usuarios del proyecto.").to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        return InternalServerError("Error al inactivar al usuario.").to_dict()


# Remove files from specific project
@main.delete('/project-files')
@verify_authentication
def delete_project_files_controller():
    try:
        requester_user = RequesterUserDto(**request.user)
        delete_project_file = DeleteProjectFileDto(**request.args)

        inactive_project_file_service(requester_user.id, delete_project_file.project, delete_project_file.file)

        Logger.add_to_events_log("info", f"Archivo {delete_project_file.file} del proyecto {delete_project_file.project} retirado por {request.user["name"]} en la cuenta {request.user["mail"]}.")

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


################# SOCKETS #################
