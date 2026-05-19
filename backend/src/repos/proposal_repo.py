from src.utilities.logger.logger import Logger
from src.models.proposal_model import Proposal, ProposalFiles, ProposalFilter, ProposalUsersModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from pymysql.cursors import DictCursor
import traceback

# Función para obtener todas las propuestas.
def get_all_propsals(session: Session, proposal: ProposalFilter):
    try:

        filters = {}

        if proposal.id is not None:
            filters["id"] = proposal.id

        if proposal.title is not None:
            filters["title"] = proposal.title

        if proposal.description is not None:
            filters["description"] = proposal.description

        if proposal.active is not None:
            filters["active"] = proposal.active

        query = select(Proposal).filter_by(**filters)

        result = session.execute(query)

        proposals = result.scalars()

        return proposals.all()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


# Función para obtener los archivos de una propuesta.
def get_propsal_files(session: Session, proposal_id: int):
    query = """SELECT filename, path FROM proposal_files_table 
    WHERE proposal_id = %s;"""
    
    cursor = None
    
    try:
        query = select(ProposalFiles.filename, ProposalFiles.path).where(proposal_id == proposal_id)
        result = session.execute(query)

        return result.all()
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


# Función para obtener los datos del usuario
def get_all_user_propsal(session: Session):
    query = "SELECT * FROM ;"
    
    cursor = None
    
    try:
        pass

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")

# Función para obtener una propuesta según su ID.
def get_propsal_by_id(session: Session, proposal_id):
    
    try:
        query = select(Proposal).where(
            Proposal.id == proposal_id
        )

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")

# Función para agregar una propuesta.
def send_propsal(session: Session, title: str, description: str):
    new_proposal = Proposal(
        title=title,
        description=description
    )

    try:
        session.add(new_proposal)
        
        session.commit()
        
        return new_proposal.id
    except Exception as ex:
        session.rollback()
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener propuestas.")


# Función para agregar un documento a una propuesta.
def add_proposal_files(session: Session, proposal_id: int, filename: str, path: str):
    try:
        new_proposal_file = ProposalFiles(
            proposal_id=proposal_id,
            filename=filename,
            path=path
        )

        session.add(new_proposal_file)

        session.flush()

        return new_proposal_file
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al cargar el archivo.")


def add_relation_user_proposal(session: Session, user_id: int, proposal_id: int):
    
    try:
        new_relation = ProposalUsersModel(
            user_id=user_id,
            proposal_id=proposal_id
        )
        
        session.add(new_relation)

        session.flush()
        
        return True
    except Exception as ex:
        raise ValueError(f"Error: {ex}")

