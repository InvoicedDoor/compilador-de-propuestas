from flask import Blueprint, request
import traceback
from ..services.auth_service import register_user
from src.models.auth_model import RegisterCredentials
from src.models.user_model import RegisterUser
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from src.utilities.logger.logger import Logger

main = Blueprint('register_blueprint', __name__)

@main.post("")
def register_route():
    try:
        data = request.get_json()

        credentials = RegisterCredentials(**data)

        user = RegisterUser(**data)

        res_service = register_user(
            user,
            credentials
        )

        return Created(res_service).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise InternalServerError('Error')