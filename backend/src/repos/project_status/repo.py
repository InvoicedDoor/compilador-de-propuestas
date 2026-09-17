from src.utilities.logger.logger import Logger
from src.dtos.project_events.dto import ProjectEventStatusDto
from src.models.users.model import UserModel
from src.models.projects.model import ProjectModel
from src.models.project_events.model import ProjectEventModel
from src.models.project_status.model import ProjectStatusModel
from src.models.project_users.model import ProjectUsersModel
from src.models.company_roles.model import CompanyRoleModel
from sqlalchemy.orm import Session
from sqlalchemy import select
import traceback


def get_status_events(session: Session, project_event: ProjectEventStatusDto):
    try:
        query = (
            select(
                UserModel.name,
                UserModel.first_lastname,
                UserModel.second_lastname,
                CompanyRoleModel.code,
                CompanyRoleModel.rol,
                ProjectEventModel.approved)
            .join(
                ProjectModel,
                ProjectModel.id == ProjectEventModel.project_id,
            )
            .join(
                UserModel,
                UserModel.id == ProjectEventModel.user_id,
            )
            .join(
                ProjectStatusModel,
                ProjectStatusModel.status == ProjectEventModel.status_code,
            )
            .join(
                CompanyRoleModel,
                CompanyRoleModel.id == UserModel.company_role_id,
            )
            .join(
                ProjectUsersModel,
                ProjectModel.id == ProjectUsersModel.project_id
            )
            .join(
                CompanyRoleModel,
                CompanyRoleModel.id == ProjectUsersModel.project_role_id,
            )
            .where(
                ProjectModel.id == project_event.project_id,
                ProjectEventModel.status_code == project_event.status_code,
                CompanyRoleModel.code.in_(project_event.approver_roles),
                CompanyRoleModel.code.in_(project_event.project_role_status_code)
            )
        )

        result = session.execute(query)

        return result.all()

    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener los eventos.")