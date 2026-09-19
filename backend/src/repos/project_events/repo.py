from src.utilities.logger.logger import Logger
from src.models.projects.model import ProjectModel 
from src.models.project_users.model import ProjectUsersModel
from src.models.project_status.model import ProjectStatusModel
from src.models.project_events.model import ProjectEventModel
from src.dtos.project_events.dto import (
    ProjectEventDto, 
    ProjectEventStatusDto
)
from src.models.users.model import UserModel
from src.models.company_roles.model import CompanyRoleModel
from src.models.project_roles.model import ProjectRoleModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update
import traceback


def get_status_events(session: Session, project_event: ProjectEventStatusDto):
    try:
        query = (
            select(
                UserModel.name,
                UserModel.first_lastname,
                UserModel.second_lastname,
                CompanyRoleModel.rol,
                CompanyRoleModel.code,
                ProjectEventModel.approved,
                )
            .join(ProjectEventModel.project_user, isouter=True)
            .join(ProjectUsersModel.users, isouter=True)
            .join(ProjectUsersModel.project, isouter=True)
            .join(ProjectUsersModel.role, isouter=True)
            .join(ProjectModel.status, isouter=True)
            .join(UserModel.role, isouter=True)
            .where(
                ProjectModel.id == project_event.project_id,
                ProjectEventModel.status_code == project_event.status_code,
                CompanyRoleModel.code.in_(project_event.approver_roles),
                ProjectRoleModel.code.in_(project_event.project_role_status_code)
            )
        )

        result = session.execute(query)

        return result.unique().fetchall()

    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener los eventos.")
    

def verify_project_approbation(session: Session, project_id, current_status):
    try:
        query = (
            select(CompanyRoleModel.code, CompanyRoleModel.rol)
            .select_from(ProjectEventModel)
            .join(ProjectEventModel.user, isouter=False)
            .join(ProjectEventModel.project, isouter=False)
            .join(UserModel.rol, isouter=False)
            .join(ProjectModel.status, isouter=False)
            .where(
                ProjectStatusModel.status == current_status,
                ProjectEventModel.project_id == project_id,
                ProjectEventModel.approved == 1
                
            ))

        result = session.execute(query)

        approbations = result.all()

        return approbations

    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar el estatus del proyecto.")


def get_user_event_project(
        session: Session, 
        event: ProjectEventDto):
    try:
        query = (select(ProjectEventModel.id)
                 .where(
                     ProjectEventModel.project_id == event.project_id,
                     ProjectEventModel.user_id == event.user_id,
                     ProjectEventModel.status_code == event.status_code
                 ))

        result = session.execute(query)

        return result.unique().scalar_one_or_none() != None
    except Exception as ex:
        Logger.add_to_system_log("error", ex)
        raise SQLAlchemyError("Error en la base de datos.")




def approve_project(
        session: Session, 
        body_approval: ProjectEventDto):
    try:
        new_event = ProjectEventModel(**body_approval.model_dump())

        session.add(new_event)

        session.flush()

        return True
    except:
        return False