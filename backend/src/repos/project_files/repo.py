from src.utilities.logger.logger import Logger
from src.models.project_files.model import ProjectFilesModel
from src.dtos.project_files.dto import (
    ProjectFilesDto, 
    )
from sqlalchemy.orm import Session
from sqlalchemy import select, update
import traceback

def get_project_files(session: Session, project_id: int):
    try:
        query = (
            select(ProjectFilesModel)
            .where(
                ProjectFilesModel.project_id == project_id,
                ProjectFilesModel.active == 1))

        result = session.execute(query)

        return result.scalars()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")


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


def inactivate_project_file(session: Session, project_id: int, file_id: int):
    try:
        query = (
            update(ProjectFilesModel)
            .where(
                ProjectFilesModel.id == file_id,
                     ProjectFilesModel.project_id == project_id,
                    ProjectFilesModel.active == 1)
            .values(active = 0))

        session.execute(query)

        session.flush()
        return True
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        return False