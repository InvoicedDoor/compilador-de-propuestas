from ..logger.logger import Logger
from ..handlers.http_exceptions import BadRequest
from traceback import format_exc
from config import MAX_SIZE
from fastapi import UploadFile

def validate_project_files(documentation: list[UploadFile]):
    errors = []
    files = []
    try:
        if documentation:
            for file in documentation:

                file.seek(0)
                size = file.size
                file.seek(0)

                if size > MAX_SIZE:
                    raise BadRequest(f"{file.filename} demasiado grande.")

                files.append(file)

            if errors:
                raise BadRequest(errors)
        return files
    except Exception:
        Logger.add_to_system_log("critical", format_exc())
        raise