from src.utilities.middlewares.verify_files import verify_extension, verify_mime, clean_name, create_secure_name
from src.dtos.project_files.dto import ProjectFilesDto
from src.dtos.mime_tipes.dto import MimeTypeDto
from src.repos.file_type_repo import get_file_type_by_filter
from src.utilities.files_manager.files_manager import process_file, write_files_function
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import Session 

load_dotenv()

documentation_path = getenv("SAVE_FILES_PATH")

def upload_files(session: Session = None, proposal_files: list = [], project_id: int = 0):
    try:
        write_files_results = []
        proposal_files_dto = []

        for file in proposal_files:
            file_saved = False
            verify_extension(file, "La propuesta se creó con éxito pero no se cargaron los archivos.")

            file_bytes = file.read()

            mime = verify_mime(file)

            if not file_bytes:
                raise BadRequest("Archivo vacío.")
                
            file_type = get_file_type_by_filter(session, MimeTypeDto(mime_pattern=mime))

            filename = clean_name(file)
            secure_name = create_secure_name(filename)

            print(secure_name)

            if len(filename) > 50:
                write_files_results.append({"status": False,"filename": filename})
                write_files_results.append(False)
                continue

            proposal_file: ProjectFilesDto = ProjectFilesDto(
                project_id=project_id, 
                filename=filename, 
                path = f"{documentation_path}/{secure_name}", 
                code=secure_name, 
                file_type_id=file_type.id)

            future = process_file(session, proposal_file)

            if not future:
                write_files_results.append({"status": False,"filename": filename})
                session.rollback()
                continue

            file_saved = write_files_function(file_bytes, proposal_file.path)

            if not file_saved:
                write_files_results.append({"status": False,"filename": filename})
                continue

            write_files_results.append({"status": True,"filename": filename})

        session.commit()
        return write_files_results

    except DomainError as domErr:
        Logger.add_to_system_log("error", domErr)
        raise domErr
    
    except Exception as e:
        Logger.add_to_system_log("error", f"Error: {e}")
        raise DomainError("Error al procesar los archivos.") 