from src.utilities.logger.logger import Logger
from src.dtos.project_files.dto import ProjectFilesDto
from src.dtos.users.dto import RequesterUserDto
from src.models.projects.model import ProjectModel
from src.models.project_users.model import ProjectUsersModel
from src.models.users.model import UserModel
from src.models.credentials.model import Auth
from src.models.project_roles.model import ProjectRoleModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from config import CAN_MODIFY_PROJECT_PROPERTIES
import traceback

def get_all_user_projects(session: Session, user_id: int, project: ProjectFilesDto):
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

def get_project_user(session: Session, requester_user: RequesterUserDto, project_id: int):
    try:
        query = (select(ProjectUsersModel.id)
                 .select_from(UserModel)
                 .join(UserModel.user_project, isouter=True)
                 .join(UserModel.credentials, isouter=True)
                 .join(ProjectUsersModel.role, isouter=True)
                 .where(
                        UserModel.id == requester_user.id,
                        Auth.mail == requester_user.mail,
                        UserModel.company_role_id == requester_user.rol,
                        ProjectUsersModel.project_id == project_id,
                        ProjectRoleModel.code.in_(CAN_MODIFY_PROJECT_PROPERTIES)
                    ))
        
        result = session.execute(query)

        user = result.unique().scalar_one_or_none()

        return user != None
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False
