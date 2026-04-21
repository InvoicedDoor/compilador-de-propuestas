from src.utilities.logger.logger import Logger
from ..repos.file_type_repo import get_file_types_repo
from traceback import format_exc

def get_file_types_service():
    try:
        file_types = get_file_types_repo()

        file_types_format = [{
            "id": type_file[0],
            "type": type_file[1],
            "description": type_file[2],
            "is_main_image": type_file[3],
            "active": type_file[4]
        } for type_file in file_types]
        return file_types_format
    except:
        Logger.add_to_log('error', format_exc())
        