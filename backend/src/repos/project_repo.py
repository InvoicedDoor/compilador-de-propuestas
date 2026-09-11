from src.utilities.logger.logger import Logger
from src.models.project_model import Project, ProjectFilesModel, ProjectUsersModel, ProjectStatusModel, ProjectEventModel
from src.dtos.project_dto import ProjectFilesDto, ProjectUsersFilter, UpdateProjectUserDto
from src.models.user_model import User, RequesterUser
from src.models.auth_model import Auth
from src.models.rol_model import Rol, ProjectRoleModel
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, and_, update
from config import CAN_MODIFY_PROJECT_PROPERTIES
import traceback

def validate_project_user(session: Session, requester_user: RequesterUser, project_id: int):
    try:
        query = (select(ProjectUsersModel.id)
                 .select_from(User)
                 .join(User.user_project, isouter=True)
                 .join(User.credentials, isouter=True)
                 .join(ProjectUsersModel.role, isouter=True)
                 .where(
                        User.id == requester_user.id,
                        Auth.mail == requester_user.mail,
                        User.rol_id == requester_user.rol,
                        ProjectUsersModel.project_id == project_id,
                        ProjectRoleModel.code.in_(CAN_MODIFY_PROJECT_PROPERTIES)
                    ))
        
        result = session.execute(query)

        user = result.unique().scalar_one_or_none()

        return user != None
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False

# Función para obtener todas las propuestas.
def get_all_project(session: Session, project: ProjectFilesDto):
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

        query = (select(Project)
                 .filter_by(**filters)
                 .join(Project.status, isouter=True))

        result = session.execute(query)

        projects = result.unique().scalars()

        return projects.all()

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

        query = (select(Project)
        .filter_by(**filters)
        .join(Project.project_user, isouter=True)
        .join(ProjectUsersModel.users, isouter=True)
        .join(ProjectUsersModel.role, isouter=True)
        .where(User.id == user_id))
        
        result = session.execute(query)

        projects = result.unique().scalars()

        return projects.all()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


def get_project_by_id(session: Session, project_id: int):
    
    try:
        query = (
            select(Project)
            .join(Project.project_user, isouter=True)
            .join(Project.project_files, isouter=True)
            .join(Project.status, isouter=True)
            .where(Project.id == project_id)
        )
        
        result = session.execute(query)

        return result.unique().scalar_one_or_none()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


def verify_project_user(session: Session, user_id: int, project_id: int):
    try:
        query = (
            select(ProjectUsersModel)
            .where(
                and_(
                    ProjectUsersModel.project_id == project_id, 
                    ProjectUsersModel.user_id == user_id,
                    ProjectUsersModel.active == 1
                    )
                )
        )

        result = session.execute(query)

        return result.unique().scalar_one_or_none()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")
    

def verify_project_approbation(session: Session, project_id, current_status):
    try:
        query = (
            select(Rol.code, Rol.rol)
            .select_from(ProjectEventModel)
            .join(ProjectEventModel.user, isouter=False)
            .join(ProjectEventModel.project, isouter=False)
            .join(User.rol, isouter=False)
            .join(Project.status, isouter=False)
            .where(
                and_(
                    ProjectStatusModel.status == current_status,
                    ProjectEventModel.project_id == project_id,
                    ProjectEventModel.approved == 1
                    )
                )
            )

        result = session.execute(query)

        approbations = result.all()

        return approbations

    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar el estatus del proyecto.")

def get_project_users(session: Session, project_users: ProjectUsersFilter = None):
    try:
        filters = {}
        if project_users.project_id is not None:
            filters["project_id"] = project_users.project_id

        query = (
            select(ProjectUsersModel)
            .join(ProjectUsersModel.users, isouter=True)
            .join(User.rol, isouter=True)
            .where(
                and_(
                    ProjectUsersModel.project_id == project_users.project_id,
                    ProjectUsersModel.active == project_users.active
                )
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
            .join(User.rol, isouter=True))

        result = session.execute(query)

        return result.unique().scalar_one_or_none()
    
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la información del usuario.")



def get_project_files(session: Session, project_id: int):
    try:
        query = (
            select(ProjectFilesModel)
            .where(
                and_(ProjectFilesModel.project_id == project_id,
                    ProjectFilesModel.active == 1)))

        result = session.execute(query)

        return result.scalars()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")


# Función para agregar una propuesta.
def send_project(session: Session, title: str, description: str):
    new_project = Project(
        title=title,
        description=description
    )

    try:
        session.add(new_project)
        
        session.commit()
        
        return new_project.id
    except Exception as ex:
        session.rollback()
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener propuestas.")


# Función para agregar un documento a una propuesta.
def add_project_files(session: Session, project_files_dto: ProjectFilesDto):
    try:
        new_project_file = ProjectFilesModel(**project_files_dto.model_dump())

        session.add(new_project_file)

        session.flush()

        return new_project_file
    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al cargar el archivo.")


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


def update_relation_user_project(
        session: Session, 
        project_user: UpdateProjectUserDto,
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
                ProjectUsersModel.user_id.in_(project_user.user_ids),
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


def inactivate_project(session: Session, project_id: int, file_id: int):
    try:
        query = (
            update(Project)
            .where(
                and_(Project.id == file_id,
                     Project.active == 1)))

        session.execute(query)

        session.flush()
        
        return True
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False
    

def inactivate_project_file(session: Session, project_id: int, file_id: int):
    try:
        query = (
            update(ProjectFilesModel)
            .where(
                and_(ProjectFilesModel.id == file_id,
                     ProjectFilesModel.project_id == project_id,
                    ProjectFilesModel.active == 1))
            .values(active = 0)
                    )

        session.execute(query)

        session.flush()
        return True
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False