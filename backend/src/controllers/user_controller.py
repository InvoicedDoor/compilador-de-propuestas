from ..services.users_service import get_users_service
from ..models.user_model import UserFilter, RequesterUser
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from flask import Blueprint, request
from src.utilities.logger.logger import Logger
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
import traceback

main = Blueprint('user_blueprint', __name__)


@main.get('')
@verify_authentication
def get_users_controller():
    try:
        user = UserFilter(**request.args)
        user_requester = RequesterUser(**request.user)

        user_info = get_users_service(user, user_requester)

        return OK("Usuarios consultados.", data=user_info).to_response()
    except:
        return InternalServerError("Error").to_dict()