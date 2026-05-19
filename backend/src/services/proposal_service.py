from ..repos.proposal_repo import add_relation_user_proposal, send_propsal, get_all_propsals, get_propsal_files
from src.utilities.handlers.http_exceptions import *
from src.utilities.middlewares.verify_files import verify_extension, verify_mime, clean_name, create_secure_name
from src.utilities.files_manager.files_manager import process_file
from src.utilities.logger.logger import Logger
from ..dtos.proposal_dto import ProposalDto
from ..models.proposal_model import ProposalFilter
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.utilities.db.db_connection import SessionLocal


BACKEND_URL = "http://localhost:5000"

def get_proposals_from_admin_service(proposal: ProposalFilter):
    session = SessionLocal()
    try:
        pass
        proposal_list = get_all_propsals(session, proposal)
        proposal_format = []

        if len(proposal_list) == 0:
            raise NotFound("No hay propuestas aún.", [])

        for data in proposal_list:
            files = [{
                "filename": file.filename,
                "source": file.path
            } for file in data.proposal_files]

            proposal_format.append({
                "title": data.title,
                "description": data.description,
                "source": files
            })

        return proposal_format
    
    except DomainError as domErr:
        return domErr
    
    except Exception as ex:
        Logger.add_to_log("error", f"Error: {ex}")
        session.rollback()
        raise UnprocessableEntity("Error al procesar los archivos.") 
    finally:
        session.close()


def get_proposals_from_users_service(proposal: ProposalFilter):
    try:
        pass
    except:
        pass

def add_proposal_service(user_id: int, proposal: ProposalDto, proposal_files):
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

        results = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            futures_map = {}

            for file in proposal_files:
                verify_extension(file, "La propuesta se creó con éxito pero no se cargaron los archivos.")

                file_bytes = file.read()

                verify_mime(file)

                if not file_bytes:
                    raise BadRequest("Archivo vacío.")


                filename = clean_name(file)
                secure_name = create_secure_name(filename)

                future = executor.submit(process_file,
                    file_bytes, 
                    proposal_id,
                    secure_name)

                futures.append(future)
                futures_map[future] = filename


            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    Logger.add_to_log("error", f"Error al procesar el archivo {futures_map[future]}: {e}")
                    results.append(False)

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