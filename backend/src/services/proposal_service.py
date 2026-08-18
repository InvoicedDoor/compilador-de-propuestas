from ..repos.proposal_repo import add_relation_user_proposal, send_propsal, get_all_propsals, get_all_user_propsal, get_propsal_by_id, verify_proposal_user, get_proposal_users, get_proposal_files, inactivate_proposal, inactivate_proposal_file
from src.utilities.files_manager.upload_files_funtion import upload_files
from ..repos.user_repo import validate_user
from src.utilities.handlers.http_exceptions import *
from src.utilities.logger.logger import Logger
from src.models.user_model import RowUser
from ..dtos.proposal_dto import ProposalDto, ImageMetadata, ProposalUserDto
from ..models.proposal_model import ProposalFilter
from src.utilities.db.db_connection import SessionLocal


BACKEND_URL = "http://localhost:5000"

def get_proposals_service(user: RowUser, proposal: ProposalFilter):
    session = SessionLocal()
    try:
        proposal_format = []
        if validate_user(user):
            proposal_list = get_all_propsals(session, proposal)

            if len(proposal_list) == 0:
                raise NotFound(message="No hay propuestas aún.", data=[])

            for data in proposal_list:
                files = [{
                    "filename": file.filename,
                    "source": file.path
                } for file in data.proposal_files]

                proposal_format.append({
                    "id": data.id,
                    "title": data.title,
                    "description": data.description,
                    "source": files
                })

        else:
            proposal_list = get_all_user_propsal(session, user.id, proposal)
            if len(proposal_list) == 0:
                raise NotFound(message="No hay propuestas aún.", data=[])

            for data in proposal_list:
                files = [{
                    "filename": file.filename,
                    "source": file.path
                } for file in data.proposal_files]

                proposal_format.append({
                    "id": data.id,
                    "title": data.title,
                    "description": data.description,
                    "source": files
                })

        return proposal_format
    
    except DomainError as domErr:
        raise domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()


def get_proposal_by_id_service(user: RowUser, proposal_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_proposal_user(session, user["id"], proposal_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        proposal = get_propsal_by_id(session, proposal_id)

        formated_proposal = {
            "id": proposal.id,
            "title": proposal.title,
            "description": proposal.description,
            "active": proposal.active,
            "files": [
            {
                "id": file.id,
                "filename": file.filename,
                "path": file.path
            } for file in proposal.proposal_files]
        }

        return formated_proposal
    
    except DomainError as domErr:
        raise domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()


def get_proposal_users_service(user: RowUser, proposal_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_proposal_user(session, user["id"], proposal_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        proposal_user: list[ProposalUserDto] = get_proposal_users(session, proposal_id)

        formated_proposal = [{
            "id": proposal_info.users.id,
            "name": " ".join(filter(None, [
                proposal_info.users.name,
                proposal_info.users.first_lastname,
                proposal_info.users.second_lastname
            ])),
            "rol": {
                "id": proposal_info.users.rol.id,
                "rol": proposal_info.users.rol.rol
            }
        } for proposal_info in proposal_user]

        return formated_proposal
    
    except DomainError as domErr:
        raise domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar la petición.") 
    finally:
        session.close()


def get_proposal_files_service(user: RowUser, proposal_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_proposal_user(session, user["id"], proposal_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        proposal_files = get_proposal_files(session, proposal_id)

        formated_proposal = [{
            "id": proposal_file.id,
            "filename": proposal_file.filename,
            "path": proposal_file.path
        } for proposal_file in proposal_files]

        return formated_proposal
    
    except DomainError as domErr:
        raise domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar la petición.") 
    finally:
        session.close()


def add_proposal_service(user_id: int, proposal: ProposalDto, proposal_files, metadata):
    session = SessionLocal()
    try:
        proposalModel: ProposalFilter = ProposalFilter(title=proposal.proposal_title,description=proposal.proposal_description,)

        exist_proposal = get_all_propsals(session, proposalModel)

        if exist_proposal:
            raise Conflict("La propuesta ya existe.")

        proposal_id = send_propsal(session, proposal.proposal_title, proposal.proposal_description)

        if not proposal_id:
            raise InternalServerError("No se pudo crear la propuesta.")

        relation_ok = add_relation_user_proposal(session, user_id, proposal_id)

        if not relation_ok:
            raise InternalServerError("No se pudo crear la relación usuario-propuesta.")
        
        if not proposal_files:
            session.commit()
            return "Propuesta vacía creada exitosamente."

        results = upload_files(proposal_files, proposal_id)
        
        if any(r is False for r in results):
            session.rollback()
            raise InternalServerError("Error insertando uno o más archivos.")
        
        session.commit()
        return "Subido correctamente."
    
    except DomainError as domErr:
        return domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 
    
    finally:
        session.close()


def add_proposal_files_service(user_id: int, proposal_id: int, proposal_files: list, metadata: list[ImageMetadata]):
    session = SessionLocal()
    try:        
        results = []

        is_valid = verify_proposal_user(session, user_id, proposal_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        results = upload_files(session, proposal_files, proposal_id)

        if any(r["status"] is True for r in results):
            session.commit()
            return "Subido correctamente."

        session.rollback()
        raise UnprocessableEntity("Error insertando uno o más archivos.")
    
    except DomainError as domErr:
        raise domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 
    
    finally:
        session.close()


def inactive_proposal_file_service(user_id: int, proposal_id: int, file_id: int):
    session = SessionLocal()
    try:
        is_valid = verify_proposal_user(session, user_id, proposal_id)

        if not is_valid:
            raise BadRequest("No puedes realizar esta acción.")

        result = inactivate_proposal_file(session, proposal_id, file_id)

        if not result:
            session.rollback()
            raise UnprocessableEntity("No se pudo eliminar el elemento.")

        session.commit()
        return "Elemento eliminado"

    except DomainError as domErr:
        raise domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise DomainError("Error al procesar los archivos.") 