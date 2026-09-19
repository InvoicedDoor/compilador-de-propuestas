from src.repos.project_users.repo import (
    add_relation_user_project, 
    verify_project_user, 
    get_project_users, 
    get_project_user, 
    update_relation_user_project,
    validate_project_user
)
from src.repos.project_roles.repo import get_role_by_code
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_users.dto import (
    ProjectUserDto, 
    UpdateProjectUserDto, 
    ProjectUsersFilter
)
from src.utilities.db.db_connection import SessionLocal

def get_project_users_service(user: RequesterUserDto, project_user_filter: ProjectUsersFilter):
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
                "id": project_info.users.role.id,
                "position": project_info.users.role.rol
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

def inactive_project_user_service(requester: RequesterUserDto, project_id, inactive_project_users: list[int]):
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