from src.utilities.logger.logger import Logger
from src.dtos.project_files.dto import ProjectFilesFilter
from src.models.projects.model import ProjectModel
from sqlalchemy.orm import Session
from sqlalchemy import select
import traceback

# Función para obtener todas las propuestas.
def get_all_projects(session: Session, project_filters: ProjectFilesFilter):
    try:
        query = (select(ProjectModel)
                 .join(ProjectModel.status, isouter=True)
                 .filter_by(**project_filters))

        result = session.execute(query)

        projects = result.unique().scalars()

        return projects.all()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")

def get_project_by_id(session: Session, project_id: int):
    
    try:
        query = (
            select(ProjectModel)
            .join(ProjectModel.project_user, isouter=True)
            .join(ProjectModel.project_files, isouter=True)
            .join(ProjectModel.status, isouter=True)
            .where(ProjectModel.id == project_id)
        )
        
        result = session.execute(query)

        return result.unique().scalar_one_or_none()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")