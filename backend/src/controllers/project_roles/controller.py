from src.services.project_roles.service import get_project_roles_service
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from flask import Blueprint, request
from src.utilities.logger.logger import Logger
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
import traceback

main_project_roles = Blueprint('project_roles_blueprint', __name__)


@main_project_roles.get('')
@verify_authentication
def verify_auth():
    project_roles = get_project_roles_service()

    return OK("Datos encontrados", project_roles).to_response()