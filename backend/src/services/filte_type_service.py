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
                    "id": file.mime_type_id,
                    "mime_pattern": file.mime_type.mime_pattern,
                    "extension": file.mime_type.extension,
                    "icon": file.mime_type.icon,
                    "category": file.mime_type.category_id
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
        