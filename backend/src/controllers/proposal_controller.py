from ..services.proposal_service import add_proposal_service, get_proposals_from_admin_service
from ..dtos.proposal_dto import ProposalDto
from ..models.proposal_model import ProposalFilter
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from jwt import decode
from flask import Blueprint, request, jsonify
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

        return jsonify({
            "data": data,
            "message": "Datos encontrados."
        })
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        return 'Error', 500

@main.post('/')
@verify_authentication
def send_proposals_route():
        data = request.form

        if not data.get('proposal_title'): 
            return jsonify({"message": "El titulo no debe estar vacío."}), 409

        files = []
        errors = []

        for file in request.files.getlist("proposal_documentation"):
            if not file:
                continue

            file.seek(0, 2)
            size = file.tell()
            file.seek(0)

            if size > MAX_SIZE:
                return jsonify({ "message": f"{file.filename} demasiado grande." })

            files.append(file)

        if errors:
            return jsonify({ "message": errors }), 400

        token = request.headers.get("Authorization")
        payload = decode(token.split(" ")[1], key, algorithms=['HS256'])
        proposal = ProposalDto(proposal_title=data["proposal_title"],
                               proposal_description=data["proposal_description"],
                               proposal_manager=payload["id"])

        service_message =  add_proposal_service(payload["id"], proposal, files)

        return jsonify({"message": service_message}), 201