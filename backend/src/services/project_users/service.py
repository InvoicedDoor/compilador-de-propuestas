from src.repos.project_users.repo import (
    add_batch_relation_user_project, 
    verify_project_user, 
    get_project_users, 
    get_batch_project_users,
    get_project_user, 
    update_relation_user_project,
    validate_project_user
)
from src.repos.project_roles.repo import get_role_by_code, get_batch_roles_by_codes
from src.repos.users.repo import get_bacth_user_by_mails
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.dtos.users.dto import RequesterUserDto
from src.dtos.project_users.dto import (
    ProjectUserDto, 
    ProjectUsersDto, 
    ProjectUsersFilter,
    AddProjectUsereDto,
    UpdateProjectUserRoleDto
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

def add_project_user_service(new_user_list: list[AddProjectUsereDto], requester: int, project_id: int):
    session = SessionLocal()
    try:
        roles = set()
        user_mails = set()
        added_user_ids = set()
        new_users_queries = []

        # Verificar que el usuario Requester pertenece al proyecto.
        is_valid = verify_project_user(session, requester, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        # Verificar que el nuevo usuario no participa en el proyecto..
        requester_role = get_project_user(session, ProjectUsersFilter(user_id=requester, project_id=project_id, active=True))

        if requester_role.role.code not in ("ADMIN", "COADMIN"):
            raise BadRequest("No tienes permisos para realizar esta acción.")

        # Verificar que el nuevo usuario no participa en el proyecto..
        for new_user in new_user_list:
            roles.add(new_user.project_role)
            user_mails.add(new_user.mail)

        project_current_users = get_batch_project_users(session, project_id)

        users_schedule = get_bacth_user_by_mails(session, list(user_mails))

        roles_schedule = get_batch_roles_by_codes(session, list(roles))

        for new_user in new_user_list:
            code = new_user.project_role
            user_mail = new_user.mail

            if user_mail in project_current_users:
                continue

            user_id = users_schedule.get(user_mail)["user_id"]
            role_id = roles_schedule.get(code)
        
            if user_id is None or role_id is None:
                continue

            if user_id in added_user_ids:
                continue

            added_user_ids.add(user_id)

            new_users_queries.append({
                "user_id": user_id,
                "project_role_id": role_id,
                "project_id": project_id
            })

        if not new_users_queries:
            raise Conflict("No se pueden agregar los elementos.")

        created = add_batch_relation_user_project(session, new_users_queries)

        if not created:
            raise Conflict("No es posible agregar la información.")
                
        session.commit()

        return f"Se agregaron {len(new_users_queries)} participantes."
    
    except DomainError:
        raise 
    
    except Exception as ex:
        Logger.add_to_system_log("error", f"Error: {ex}")
        session.rollback()
        raise InternalServerError("Error al asignar al personal. Consulte con el administrador del sistema.") 
    
    finally:
        session.close()

def update_project_user_service(update_user_dto: UpdateProjectUserRoleDto, requester: int, project_id: int):
    session = SessionLocal()
    try:
        results = 0
        roles = {}

        is_valid = verify_project_user(session, requester, project_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        requester_role = get_project_user(session, ProjectUsersFilter(user_id=requester, project_id=project_id, active=True))

        if requester_role.role.code not in ("ADMIN", "COADMIN"):
            raise BadRequest("No tienes permisos para realizar esta acción.")

        code = update_user_dto.project_role

        if code not in roles:
            roles[code] = get_role_by_code(session, code)

        user_role = roles[code]

        if not user_role:
            raise BadRequest("No puedes usar este rol.")

        project_user = get_project_user(session, ProjectUsersFilter(project_id=project_id, user_id=update_user_dto.user_id, active=True))

        if project_user is None:
            raise BadRequest("El usuario no participa en el proyecto.")

        update_user = ProjectUserDto(
            project_id=project_id,
            user_id=update_user_dto.user_id,
            project_role_id=user_role,
            active=True
        )

        updated = update_relation_user_project(session, update_user, requester)

        if not updated:
            session.rollback()
            raise Conflict("No se ha actualizado el recurso.")

        session.commit()
        return f"Se actualizó correctamente."
    
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

        to_inactive_request = ProjectUsersDto(
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