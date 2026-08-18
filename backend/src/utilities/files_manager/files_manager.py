from src.repos.proposal_repo import add_proposal_files
from src.models.proposal_model import ProposalFilesDto
from werkzeug.datastructures import FileStorage
from src.utilities.logger.logger import Logger
from sqlalchemy.orm import Session
from traceback import format_exc
from shutil import copyfileobj
from dotenv import load_dotenv
from os.path import exists

def write_files_function(file_bytes, path: str) -> bool:
    try:
        if exists(path):
            return False
        
        with open(path, "wb") as buffer:
            buffer.write(file_bytes)

        return True
    except:
        Logger.add_to_log("error", format_exc())
        return False
    

def process_file(session: Session, proposal_file: ProposalFilesDto):
    try:
        db_saved = add_proposal_files(session, proposal_file)

        if not db_saved:
            Logger.add_to_log("info", "No se guardó el registro en la base de datos.")
            return False

        Logger.add_to_log("info", "Registro guardado en la base de datos")

        return True
    except:
        Logger.add_to_log("error", format_exc())
        return False