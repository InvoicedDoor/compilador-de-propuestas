from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from src.services.file_tipes.service import get_file_tipes_service
from fastapi import APIRouter, Depends
from src.utilities.logger.logger import Logger
import traceback

file_tipes_routes = APIRouter()

@file_tipes_routes.get('')
def get_all_file_tipes_route(
    _: None = Depends(verify_authentication)
):
    try:
        file_types = get_file_tipes_service()

        return OK("Datos encontrados.", file_types).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')
