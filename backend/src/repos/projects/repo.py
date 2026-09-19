from src.utilities.logger.logger import Logger
from src.models.projects.model import ProjectModel 
from src.dtos.project_files.dto import ProjectFilesDto
from sqlalchemy.orm import Session
from sqlalchemy import select, update
import traceback

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

        query = (select(ProjectModel)
                 .filter_by(**filters)
                 .join(ProjectModel.status, isouter=True))

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

# Función para agregar una propuesta.
def send_project(session: Session, title: str, description: str):
    new_project = ProjectModel(
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

def inactivate_project(session: Session, project_id: int, file_id: int):
    try:
        query = (
            update(ProjectModel)
            .where(
                ProjectModel.id == file_id,
                ProjectModel.active == 1))

        session.execute(query)

        session.flush()
        
        return True
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False