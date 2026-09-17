from src.repos.project_repo import add_project_files
from src.dtos.project_files.dto import ProjectFilesDto
from src.utilities.logger.logger import Logger
from sqlalchemy.orm import Session
from traceback import format_exc
from os.path import exists

def write_files_function(file_bytes, path: str) -> bool:
    try:
        if exists(path):
            return False
        
        with open(path, "wb") as buffer:
            buffer.write(file_bytes)

        return True
    except:
        Logger.add_to_system_log("error", format_exc())
        return False
    

def process_file(session: Session, project_file: ProjectFilesDto):
    try:
        db_saved = add_project_files(session, project_file)

        if not db_saved:
            Logger.add_to_system_log("info", "No se guardó el registro en la base de datos.")
            return False

        Logger.add_to_system_log("info", "Registro guardado en la base de datos")

        return True
    except:
        Logger.add_to_system_log("error", format_exc())
        return False