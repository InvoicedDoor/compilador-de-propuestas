from src.utilities.logger.logger import Logger
from src.dtos.roles_dto import ProjectRol
from src.models.rol_model import ProjectRoleModel
from sqlalchemy.orm import Session
from sqlalchemy import select, update
import traceback



# Función para obtener todas las propuestas.
def get_all_roles(session: Session, roles_filter: ProjectRol):
    try:

        filters = {}

        if roles_filter.code is not None:
            filters["code"] = roles_filter.code

        query = (select(ProjectRoleModel.id)
                 .filter_by(**filters))

        result = session.execute(query)

        projects = result.unique().scalars()

        return projects.all()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


# Función para obtener todas las propuestas.
def get_role_by_code(session: Session, role_code: str):
    try:
        query = (select(ProjectRoleModel.id)
                 .where(ProjectRoleModel.code == role_code))

        result = session.execute(query)

        role = result.scalar_one_or_none()

        return role

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")