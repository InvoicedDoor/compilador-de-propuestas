from ..services.proposal_service import add_proposal_service, get_proposals_service, get_proposal_by_id_service, add_proposal_files_service, get_proposal_users_service, get_proposal_files_service, inactive_proposal_file_service
from ..dtos.proposal_dto import ProposalDto, DeleteProposalFileDto
from ..models.proposal_model import ProposalFilter
from ..models.user_model import RowUser
from src.utilities.logger.logger import Logger
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from jwt import decode
from json import loads
from config import Config
from webargs import fields
from pydantic import ValidationError
from flask import Blueprint, request
from webargs.flaskparser import use_args
import traceback

main = Blueprint('proposal_blueprint', __name__)

key = Config.SECRET_KEY
MAX_SIZE = 5 * 1024 * 1024

@main.get('')
@verify_authentication
def get_all_proposals_route():
    try:
        proposal: ProposalFilter = ProposalFilter()

        data = get_proposals_service(RowUser(**request.user), proposal)

        return OK("Datos encontrados.", data).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise InternalServerError('Error')
    

@main.get('/proposal-users/<int:id>')
@verify_authentication
def get_proposal_users_route(id: int):
    try:
        proposal = get_proposal_users_service(request.user, proposal_id=id)
        return OK("Datos encontrados.", proposal).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        return InternalServerError('Error')
    

@main.get('/proposal-files/<int:id>')
@verify_authentication
def get_proposal_files_route(id: int):
    try:
        proposal = get_proposal_files_service(request.user, proposal_id=id)
        return OK("Datos encontrados.", proposal).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        return InternalServerError('Error')
    


@main.get('/<int:id>')
@verify_authentication
def get_proposal_by_id_route(id: int):
    try:
        proposal = get_proposal_by_id_service(request.user, proposal_id=id)
        return OK("Datos encontrados.", proposal).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        return InternalServerError('Error')


@main.post('')
@verify_authentication
def send_proposals_route():
    metadata_count = 0
    metadata = []
    try:
        data = request.form

        metadata_raw = request.form.get("metadata")
        documentation = request.files.getlist("proposal_documentation")

        if not data.get('proposal_title'): 
            raise BadRequest("El titulo no debe estar vacío.")

        errors = []
        files = []

        if metadata_raw and documentation:
            metadata = loads(metadata_raw)

            for file in documentation:
                if not file or not metadata[metadata_count]:
                    continue

                file.seek(0, 2)
                size = file.tell()
                file.seek(0)

                if size > MAX_SIZE:
                    raise BadRequest(f"{file.filename} demasiado grande.")

                files.append(file)

                metadata_count += 1

            if errors:
                raise BadRequest(errors)
            
        proposal = ProposalDto(proposal_title=data["proposal_title"],
        proposal_description=data["proposal_description"],
        proposal_manager=request.user["id"])

        service_message = add_proposal_service(request.user["id"], proposal, files, metadata)

        return Created(message=service_message).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_log('error', traceback.format_exc())
        return InternalServerError('Error')
    

@main.post('/<int:id>')
@verify_authentication
def add_proposal_files_route(id):
    metadata_count = 0
    metadata = []
    try:
        documentation = request.files.getlist("proposal_documentation")

        errors = []
        files = []

        if documentation:
            for file in documentation:
                if not file:
                    continue

                file.seek(0, 2)
                size = file.tell()
                file.seek(0)

                if size > MAX_SIZE:
                    raise BadRequest(f"{file.filename} demasiado grande.")

                files.append(file)

                metadata_count += 1

            if errors:
                raise BadRequest(errors)
            
        service_message = add_proposal_files_service(request.user["id"], id, files, metadata)

        return Created(message=service_message).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception:
        Logger.add_to_log('error', traceback.format_exc())
        return InternalServerError('Error').to_dict()

delete_args = {
    "proposal": fields.Int(required=True),
    "files": fields.Int(required=True)
}

@main.delete('/proposal-files')
@verify_authentication
def delete_proposal_files_route():
    try:
        delete_proposal_file = DeleteProposalFileDto(**request.args)

        inactive_proposal_file_service(request.user["id"], delete_proposal_file.proposal, delete_proposal_file.file)

        return OK("Elemento eliminado.").to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except ValidationError as ve:
        count = 1
        response_string = "Campos incorrectos: "
        errors = ve.errors()
        for error in errors:
            field = error["loc"][0]
            message = error["msg"]
            print(message)
            if count < len(errors):
                response_string += f"{field} ({message}), "
                count += 1
            else: 
                count += 1
                response_string += f"{field} ({message})"

        return BadRequest(response_string).to_dict()

    except Exception as e:
        Logger.add_to_log('error', traceback.format_exc())
        return InternalServerError("Error").to_dict()