from ..services.auth_service import auth_service, change_password_service
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from flask import Blueprint, request, jsonify
from src.utilities.logger.logger import Logger
from config import routes
import traceback

main = Blueprint('auth_blueprint', __name__)


@main.get('')
@verify_authentication
def verify_auth():
    return jsonify({ "message": "Authorized" })


@main.post('')
def auth_route():
    try:
        mail = request.json['mail']
        password = request.json['password']
        return auth_service(mail, password)
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        return {"message": 'Error'}, 500


@main.post("/change-password/")
def change_password_route():
    try:
        mail = request.json["mail"]
        old_password = request.json['old_password']
        new_password = request.json['new_password']
        new_password_confirmation = request.json['new_password_confirmation']

        return change_password_service(mail, old_password, new_password, new_password_confirmation)
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        return {"message": 'Error'}, 500