from src.utilities.logger.logger import Logger
from src.models.project_roles.model import ProjectRoleModel
from sqlalchemy.orm import Session
from sqlalchemy import select, update
import traceback


def get_project_roles(session: Session):
    try:
        query = (select(ProjectRoleModel))

        result = session.execute(query)

        project_roles = result.scalars()

        return project_roles.all()
    except:
        Logger.add_to_system_log("error", traceback.format_exc())
        return False