from src.repos.proposal_repo import add_proposal_files
from werkzeug.datastructures import FileStorage
from src.utilities.logger.logger import Logger
from traceback import format_exc
from shutil import copyfileobj
from dotenv import load_dotenv
from os.path import exists
from os import getenv

load_dotenv()

documentation_path = getenv("SAVE_FILES_PATH")

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
    

def process_file(file_bytes, proposal_id: int, filename: str):
    try:
        path = f"{documentation_path}/{filename}"

        file_saved = write_files_function(file_bytes, path)

        if not file_saved:
            return False

        db_saved = add_proposal_files(proposal_id, filename, path)

        if not db_saved:
            Logger.add_to_log("info", "No se guardó el registro en la base de datos.")

        Logger.add_to_log("info", "Registro guardado en la base de datos")

        return db_saved
    except:
        Logger.add_to_log("error", format_exc())