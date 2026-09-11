from ..repos.project_repo import add_relation_user_project, send_project, get_all_project, get_all_user_project, get_project_by_id, verify_project_user, get_project_users, get_project_user, get_project_files, update_relation_user_project, inactivate_project_file, verify_project_approbation, validate_project_user
from ..repos.roles_repo import get_role_by_code
from ..repos.user_repo import get_user_by_id
from src.utilities.files_manager.upload_files_funtion import upload_files
from ..repos.user_repo import validate_user
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.models.user_model import RequesterUser
from ..dtos.project_dto import ProjectDto, ImageMetadata, ProjectUserDto, ProjectFilter, ProjectEventDto, UpdateProjectUserDto, ProjectUsersFilter
from ..dtos.roles_dto import ProjectRol
from src.utilities.db.db_connection import SessionLocal
from config import ALTERNATIVE_STATUS, APROVAL_STEPS, CLOSER_STATUS


BACKEND_URL = "http://localhost:5000"

def get_projects_service(user: RequesterUser, project: ProjectFilter):
    session = SessionLocal()
    try:
        project_format = []
        if validate_user(user):
            project_list = get_all_project(session, project)
        else:
            project_list = get_all_user_project(session, user.id, project)

        if len(project_list) == 0:
            raise NotFound(message="No hay propuestas aún.", data=[])

        for data in project_list:
            files = [{
                "filename": file.filename,
                "source": file.path
            } for file in data.project_files]

            project_format.append({
                "id": data.id,
                "title": data.title,
                "description": data.description,
                "status": {
                    "code": data.status.status,
                    "description": data.status.description
                },
                "source": files
            })
        return project_format
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()


def get_project_by_id_service(user: RequesterUser, project_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_project_user(session, user.id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        project = get_project_by_id(session, project_id)

        formated_project = {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "active": project.active,
            "files": [
            {
                "id": file.id,
                "filename": file.filename,
                "path": file.path
            } for file in project.project_files]
        }

        return formated_project
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()


def get_project_users_service(user: RequesterUser, project_user_filter: ProjectUsersFilter):
    session = SessionLocal()
    try:
        is_valid = verify_project_user(session, user.id, project_user_filter.project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        project_user = get_project_users(session, project_user_filter)

        formated_project = [{
            "id": project_info.users.id,
            "name": " ".join(filter(None, [
                project_info.users.name,
                project_info.users.first_lastname,
                project_info.users.second_lastname
            ])),
            "position": {
                "id": project_info.users.rol.id,
                "position": project_info.users.rol.rol
            },
            "rol": {
                "id": project_info.role.code,
                "rol": project_info.role.description
            }
        } for project_info in project_user]

        return formated_project
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar la petición.") 
    finally:
        session.close()


def get_project_files_service(user: RequesterUser, project_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_project_user(session, user.id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        project_files = get_project_files(session, project_id)

        formated_project = [{
            "id": project_file.id,
            "filename": project_file.filename,
            "path": project_file.path
        } for project_file in project_files]

        return formated_project
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar la petición.") 
    finally:
        session.close()


def add_project_service(user_id: int, project: ProjectDto, project_files, metadata):
    session = SessionLocal()
    try:
        projectModel: ProjectFilter = ProjectFilter(title=project.project_title,description=project.project_description,)

        exist_project = get_all_project(session, projectModel)

        if exist_project:
            raise Conflict("La propuesta ya existe.")

        project_id = send_project(session, project.project_title, project.project_description)

        if not project_id:
            raise InternalServerError("No se pudo crear la propuesta.")

        relation_ok = add_relation_user_project(session, user_id, project_id, project_role_id = 1)

        if not relation_ok:
            raise InternalServerError("No se pudo crear la relación usuario-propuesta.")
        
        if not project_files:
            session.commit()
            return "Propuesta vacía creada exitosamente."

        results = upload_files(project_files, project_id)
        
        if any(r is False for r in results):
            session.rollback()
            raise InternalServerError("Error insertando uno o más archivos.")
        
        session.commit()
        return "Subido correctamente."
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 
    
    finally:
        session.close()


def add_project_files_service(user_id: int, project_id: int, project_files: list, metadata: list[ImageMetadata]):
    session = SessionLocal()
    try:        
        results = []

        is_valid = verify_project_user(session, user_id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        results = upload_files(session, project_files, project_id)

        if any(r["status"] is True for r in results):
            session.commit()
            return "Subido correctamente."

        session.rollback()
        raise UnprocessableEntity("Error insertando uno o más archivos.")
    
    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 
    
    finally:
        session.close()


def add_project_user_service(new_user_list: list[ProjectUserDto], requester: int, project_id: int):
    session = SessionLocal()
    try:
        results = 0
        roles = {}

        is_valid = verify_project_user(session, requester, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        requester_role = get_project_user(session, ProjectUsersFilter(user_id=requester, project_id=project_id))

        if requester_role.role.code not in ("ADMIN", "COADMIN"):
            raise BadRequest("No tienes permisos para realizar esta acción.")

        for new_user in new_user_list:
            code = new_user["project_role"]

            if code not in roles:
                roles[code] = get_role_by_code(session, code)

            user_role = roles[code]

            if not user_role:
                continue

            project_user = get_project_user(session, ProjectUsersFilter(project_id=project_id, user_id=new_user["user_id"]))

            if project_user is None:
                created = add_relation_user_project(session, new_user["user_id"], project_id, user_role)

                if created:
                    results += 1

        if results > 0:
            session.commit()
            return f"Se agregaron {results} participantes."

        session.rollback()

        raise UnprocessableEntity("El personal ya participa en el proyecto."
        )
    
    except DomainError:
        raise 
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise InternalServerError("Error al asignar al personal. Consulte con el administrador del sistema.") 
    
    finally:
        session.close()


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
            for step in range(len(APROVAL_STEPS)):
                if APROVAL_STEPS[f"STEP_{step + 1}"]["status"] == project.status.status:
                    current_step = step+1
                    APPROVAL_PERSON = APROVAL_STEPS[f"STEP_{step + 1}"]["approver"]

            # Validate correct next step
            if status != APROVAL_STEPS[f"STEP_{current_step + 1}"]["status"]:
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


def update_project_user_service(update_user_list: UpdateProjectUserDto, requester: int, project_id: int):
    session = SessionLocal()
    try:
        results = 0
        roles = {}

        is_valid = verify_project_user(session, requester, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        requester_role = get_project_user(session, ProjectUsersFilter(user_id=requester, project_id=project_id))

        if requester_role.role.code not in ("ADMIN", "COADMIN"):
            raise BadRequest("No tienes permisos para realizar esta acción.")

        for update_user in update_user_list:
            code = update_user["project_role"]

            if code not in roles:
                roles[code] = get_role_by_code(session, code)

            user_role = roles[code]

            if not user_role:
                continue

            project_user = get_project_user(session, ProjectUsersFilter(project_id=project_id, user_id=update_user["user_id"]))

            if project_user is None:
                continue

            updated = update_relation_user_project(session, project_id, update_user)

            if updated:
                results += 1

        if results > 0:
            session.commit()
            return f"Se actualizaron {results} participantes."

        session.rollback()

        raise UnprocessableEntity("El personal no participa en el proyecto."
        )
    
    except DomainError:
        raise 
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise InternalServerError("Error al asignar al personal. Consulte con el administrador del sistema.") 
    
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
            for step in range(len(APROVAL_STEPS)):
                if APROVAL_STEPS[f"STEP_{step+1}"]["status"] == project.status.status:
                    current_step = step+1

            # Validate correct next step
            if status != APROVAL_STEPS[f"STEP_{current_step + 1}"]["status"]:
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


def inactive_project_file_service(user_id: int, project_id: int, file_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_project_user(session, user_id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        result = inactivate_project_file(session, project_id, file_id)

        if not result:
            session.rollback()
            raise UnprocessableEntity("No se pudo eliminar el elemento.")

        session.commit()

        return "Elemento eliminado"

    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 

    finally:
        session.close()

def inactive_project_user_service(requester: RequesterUser, project_id, inactive_project_users: list[int]):
    session = SessionLocal()
    results = 0
    filters = {}

    try:
        is_valid = verify_project_user(session, requester.id, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción. No eres partícipe en el proyecto.")

        requester_is_admin = validate_project_user(session, requester, project_id)

        if not requester_is_admin:
            raise BadRequest("No puedes realizar esta acción. No eres administrador del proyecto.")

        to_inactive_request = UpdateProjectUserDto(
            user_ids=inactive_project_users, project_id=project_id,
            active=False
        )

        result = update_relation_user_project(session,to_inactive_request, requester.id)

        if not result:
            raise UnprocessableEntity("No se pudo eliminar a los usuarios.")

        session.commit()

        return f"Se eliminaron {results} usuarios."

    except DomainError:
        raise
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar la petición.") 

    finally:
        session.close()