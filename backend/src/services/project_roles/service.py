from src.utilities.logger.logger import Logger
from src.repos.project_roles.repo import get_project_roles
from src.utilities.db.db_connection import SessionLocal
import traceback

def get_project_roles_service():
    session = SessionLocal()
    try:
        row_project_roles = get_project_roles(session)
        project_roles = [{
            "code": project_role.code,
            "description": project_role.description
        } for project_role in row_project_roles]

        return project_roles
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
    finally:
        session.close()