from ..services.auth_service import auth_service, change_password_service
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from flask import Blueprint, request
from src.utilities.logger.logger import Logger
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
import traceback

main = Blueprint('auth_blueprint', __name__)


@main.get('')
@verify_authentication
def verify_auth():
    return OK("Authorized").to_response()


@main.post('')
def auth_route():
    try:
        mail = request.json['mail']
        password = request.json['password']
        res_service = auth_service(mail, password)

        return OK(data=res_service).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()
    
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise InternalServerError('Error')


@main.post("/change-password")
def change_password_route():
    try:
        mail = request.json["mail"]
        old_password = request.json['old_password']
        new_password = request.json['new_password']
        new_password_confirmation = request.json['new_password_confirmation']

        res_service = change_password_service(mail, old_password, new_password, new_password_confirmation)

        return OK(res_service).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise InternalServerError('Error')
    