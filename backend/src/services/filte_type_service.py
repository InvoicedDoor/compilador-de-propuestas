from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from ..repos.file_type_repo import get_file_tipes_repo
from src.utilities.logger.logger import Logger
from src.utilities.db.db_connection import SessionLocal
from traceback import format_exc

def get_file_tipes_service():
    session = SessionLocal()
    try:

        file_types = get_file_tipes_repo(session)

        return [
            {
                "id": file.id,
                "description": file.description,
                "mime": {
                    "id": file.mime.id,
                    "mime_pattern": file.mime.mime_pattern,
                    "extension": file.mime.extension,
                    "icon": file.mime.icon,
                    "category": file.mime.category
                },
                "is_main_image": file.is_main_image,
                "active": file.active
            }
            for file in file_types
        ]
    
    except DomainError as domErr:
        raise domErr

    except:

        Logger.add_to_log(
            'error',
            format_exc()
        )

    finally:
        session.close()
        