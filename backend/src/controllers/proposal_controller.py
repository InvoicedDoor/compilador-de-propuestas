from ..services.proposal_service import add_proposal_service, get_proposals_from_admin_service
from ..dtos.proposal_dto import ProposalDto
from ..models.proposal_model import ProposalFilter
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from jwt import decode
from flask import Blueprint, request
from config import Config
import traceback

main = Blueprint('proposal_blueprint', __name__)

key = Config.SECRET_KEY
MAX_SIZE = 5 * 1024 * 1024

@main.get('')
@verify_authentication
def get_all_proposals_route():
    try:
        proposal: ProposalFilter = ProposalFilter()
        data = get_proposals_from_admin_service(proposal)

        return OK("Datos encontrados.", data).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise InternalServerError('Error')

@main.post('/')
@verify_authentication
def send_proposals_route():
    try:
        data = request.form

        if not data.get('proposal_title'): 
            raise BadRequest("El titulo no debe estar vacío.")

        files = []
        errors = []

        for file in request.files.getlist("proposal_documentation"):
            if not file:
                continue

            file.seek(0, 2)
            size = file.tell()
            file.seek(0)

            if size > MAX_SIZE:
                raise BadRequest(f"{file.filename} demasiado grande.")

            files.append(file)

        if errors:
            raise BadRequest(errors)

        token = request.headers.get("Authorization")
        payload = decode(token.split(" ")[1], key, algorithms=['HS256'])
        proposal = ProposalDto(proposal_title=data["proposal_title"],
        proposal_description=data["proposal_description"],
        proposal_manager=payload["id"])

        service_message =  add_proposal_service(payload["id"], proposal, files)

        return Created(service_message).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_log('error', traceback.format_exc())
        raise InternalServerError('Error')