from src.utilities.logger.logger import Logger
from .dto import GetProject, AddProject, UpdateProject
from .model import ProjectModel
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, update
import traceback


# Función para obtener todas las propuestas.
def get_all_project(session: Session, project: GetProject):
    try:

        filters = {}
        if project.title is not None:
            filters["title"] = project.title

        if project.priority is not None:
            filters["priority"] = project.priority

        if project.status_id is not None:
            filters["status_id"] = project.status_id

        if project.active is not None:
            filters["active"] = project.active

        query = (select(ProjectModel)
                 .filter_by(**filters)
                 .join(ProjectModel.status, isouter=True))

        result = session.execute(query)

        projects = result.scalars()

        return projects.all()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


# Función para obtener un proyecto por Id.
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
def send_project(session: Session, new_project: AddProject):
    try:
        session.add(new_project)
        
        session.commit()
        
        return new_project.id
    except Exception as ex:
        session.rollback()
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener propuestas.")


# Función para actualizar la información de un proyecto.
def update_project(session: Session, project_update: UpdateProject, project_id: int):
    values = {}

    try:
        if project_update.title:
            values["title"] = project_update.title

        if project_update.description:
            values["description"] = project_update.description

        if project_update.main_directory:
            values["main_directory"] = project_update.main_directory

        if project_update.priority:
            values["priority"] = project_update.priority

        if project_update.status_id:
            values["status_id"] = project_update.status_id

        if project_update.active:
            values["active"] = project_update.active

        query = (update(ProjectModel)
                 .values(values)
                 .where(ProjectModel.id == project_id))
        
        result = session.execute(query)
        
        session.commit()
        
        return result.rowcount > 0
    except Exception as ex:
        session.rollback()
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener propuestas.")


# Función para inactivar un proyecto.
def inactivate_project(session: Session, project_status: bool, project_id: int):
    values = {}

    try:
        values["active"] = project_status

        query = (update(ProjectModel)
                 .values(values)
                 .where(
                     and_(
                         ProjectModel.id == project_id,
                         ProjectModel.active == 1
                     )))
        
        result = session.execute(query)
        
        session.commit()
        
        return result.rowcount > 0
    except Exception as ex:
        session.rollback()
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al obtener propuestas.")