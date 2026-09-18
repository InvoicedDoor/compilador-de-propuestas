
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from ..services.filte_type_service import get_file_tipes_service
from fastapi import Request, APIRouter
from src.utilities.logger.logger import Logger
import traceback

file_tipes_routes = APIRouter()

@file_tipes_routes.get('')
@verify_authentication
def get_all_file_tipes_route():
    try:
        file_types = get_file_tipes_service()

        return OK("Datos encontrados.", file_types).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')
