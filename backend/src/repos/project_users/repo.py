from src.utilities.logger.logger import Logger
from src.models.projects.model import ProjectModel 
from src.models.project_users.model import ProjectUsersModel
from src.dtos.project_files.dto import ProjectFilesDto
from src.dtos.project_users.dto import (
    ProjectUsersFilter, 
    ProjectUserDto
)
from src.dtos.company_roles.dto import ValidationUserRoleDto
from src.models.users.model import UserModel
from src.dtos.users.dto import RequesterUserDto
from src.models.credentials.model import Auth
from src.models.project_roles.model import ProjectRoleModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, insert
from config import CAN_MODIFY_PROJECT_PROPERTIES
import traceback

def validate_project_user(session: Session, requester_user: RequesterUserDto, project_id: int):
    try:
        query = (select(ProjectUsersModel.id)
                 .select_from(UserModel)
                 .join(UserModel.user_project, isouter=True)
                 .join(UserModel.credentials, isouter=True)
                 .join(ProjectUsersModel.role, isouter=True)
                 .where(
                        UserModel.id == requester_user.id,
                        Auth.mail == requester_user.mail,
                        UserModel.rol_id == requester_user.rol,
                        ProjectUsersModel.project_id == project_id,
                        ProjectRoleModel.code.in_(CAN_MODIFY_PROJECT_PROPERTIES)
                    ))
        
        result = session.execute(query)

        user = result.unique().scalar_one_or_none()

        return user != None
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False

def verify_project_user(session: Session, user_id: int, project_id: int):
    try:
        query = (
            select(ProjectUsersModel)
            .where(
                ProjectUsersModel.project_id == project_id, 
                ProjectUsersModel.user_id == user_id,
                ProjectUsersModel.active == 1
            )
        )

        result = session.execute(query)

        return result.unique().scalar_one_or_none()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")

def validate_user_project_role(session: Session, validate_data: ValidationUserRoleDto):
    try:
        query = (select(ProjectRoleModel.id)
                 .select_from(ProjectUsersModel)
                 .join(ProjectUsersModel.role, isouter=True)
                 .where(
                     ProjectRoleModel.code.in_(validate_data.project_roles),
                     ProjectUsersModel.user_id == validate_data.user_id,
                     ProjectUsersModel.project_id == validate_data.project_id
                     ))

        result = session.execute(query)

        role = result.scalar_one_or_none()

        return role
    
    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")

def get_all_user_project(session: Session, user_id: int, project: ProjectFilesDto):
    try:
        filters = {}

        if project.id is not None:
            filters["id"] = project.id

        if project.title is not None:
            filters["title"] = project.title

        if project.description is not None:
            filters["description"] = project.description

        if project.active is not None:
            filters["active"] = project.active

        query = (select(ProjectModel)
        .filter_by(**filters)
        .join(ProjectModel.project_user, isouter=True)
        .join(ProjectUsersModel.users, isouter=True)
        .join(ProjectUsersModel.role, isouter=True)
        .where(UserModel.id == user_id))
        
        result = session.execute(query)

        projects = result.unique().scalars()

        return projects.all()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")

def get_project_users(session: Session, project_users: ProjectUsersFilter = None):
    try:
        filters = {}
        if project_users.project_id is not None:
            filters["project_id"] = project_users.project_id

        query = (
            select(ProjectUsersModel)
            .join(ProjectUsersModel.users, isouter=True)
            .join(UserModel.role, isouter=True)
            .where(
                ProjectUsersModel.project_id == project_users.project_id,
                ProjectUsersModel.active == project_users.active
            ))

        result = session.execute(query)

        data = result.unique().scalars()

        return data.all()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")

def get_project_user(session: Session, project_user_filter: ProjectUsersFilter):
    try:
        filters = {}

        if project_user_filter.user_id is not None:
            filters["user_id"] = project_user_filter.user_id

        if project_user_filter.project_role_id is not None:
            filters["project_role_id"] = project_user_filter.project_role_id

        if project_user_filter.project_id is not None:
            filters["project_id"] = project_user_filter.project_id

        if project_user_filter.active is not None:
            filters["active"] = project_user_filter.active

        query = (
            select(ProjectUsersModel)
            .filter_by(**filters)
            .join(ProjectUsersModel.users, isouter=True)
            .join(ProjectUsersModel.role, isouter=True)
            .join(UserModel.role, isouter=True))

        result = session.execute(query)

        return result.unique().scalar_one_or_none()
    
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la información del usuario.")

def get_project_users(session: Session, project_user_filter: ProjectUsersFilter):
    try:
        filters = {}

        if project_user_filter.user_id is not None:
            filters["user_id"] = project_user_filter.user_id

        if project_user_filter.project_role_id is not None:
            filters["project_role_id"] = project_user_filter.project_role_id

        if project_user_filter.project_id is not None:
            filters["project_id"] = project_user_filter.project_id

        if project_user_filter.active is not None:
            filters["active"] = project_user_filter.active

        query = (
            select(ProjectUsersModel)
            .filter_by(**filters)
            .join(ProjectUsersModel.users, isouter=True)
            .join(ProjectUsersModel.role, isouter=True)
            .join(UserModel.role, isouter=True))

        result = session.execute(query)

        return result.unique().scalars().all()
    
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la información del usuario.")

def get_batch_project_users(session: Session, project_id: int):
    try:
        query = (select(ProjectUsersModel.user_id,
                        Auth.mail)
                 .join(ProjectUsersModel.users)
                 .join(UserModel.credentials)
                 .where(ProjectUsersModel.project_id == project_id))

        result = session.execute(query)

        project_users_list = result.mappings().all()

        fromated_project_users = {
            project_user["mail"]: project_user["user_id"]
            for project_user in project_users_list
        }
        
        return fromated_project_users
    
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la información del usuario.")

def add_relation_user_project(session: Session, user_id: int, project_id: int, project_role_id: int):
    
    try:
        new_relation = ProjectUsersModel(
            user_id=user_id,
            project_id=project_id,
            project_role_id = project_role_id
        )
        
        session.add(new_relation)

        session.flush()
        
        return True
    except Exception as ex:
        raise ValueError(f"Error: {ex}")

def add_batch_relation_user_project(session: Session, project_user_list: list[ProjectUserDto]):
    
    try:
        stmt = insert(ProjectUsersModel).values(project_user_list)
        
        session.execute(stmt)

        session.flush()
        
        return True
    except Exception as ex:
        raise ValueError(f"Error: {ex}")

def update_relation_user_project(
        session: Session, 
        project_user: ProjectUserDto,
        requester_id: int):
    
    try:
        values = {}

        filters = {
            "project_id": project_user.project_id
        }

        if project_user.project_role_id is not None:
            values["project_role_id"] = project_user.project_role_id

        if project_user.active is not None:
            values["active"] = project_user.active

        query = (
            update(ProjectUsersModel)
            .where(
                ProjectUsersModel.user_id == project_user.user_id,
                ProjectUsersModel.project_id == project_user.project_id,
                ProjectUsersModel.user_id != requester_id)
            .values(**values)
        )

        res = session.execute(query)

        Logger.add_to_test_log("info", query)

        session.flush()
        
        return res.rowcount > 0
    
    except SQLAlchemyError:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False

    except Exception as ex:
        raise ValueError(f"Error: {ex}")
