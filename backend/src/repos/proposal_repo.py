from src.utilities.logger.logger import Logger
from src.models.proposal_model import Proposal, ProposalFiles, ProposalFilter, ProposalUsersModel, ProposalFilesDto
from src.models.user_model import User
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_, update
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
    
def get_all_user_propsal(session: Session, user_id: int, proposal: ProposalFilter):
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

        query = (select(Proposal)
        .filter_by(**filters)
        .join(Proposal.proposal_user, isouter=True)
        .join(ProposalUsersModel.users, isouter=True)
        .where(User.id == user_id))
        

        result = session.execute(query)

        proposals = result.unique().scalars()

        return proposals.all()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


# # Función para obtener los archivos de una propuesta.
# def get_propsal_files(session: Session, proposal_id: int):
#     query = """SELECT filename, path FROM proposal_files_table 
#     WHERE proposal_id = %s;"""
    
#     cursor = None
    
#     try:
#         query = select(ProposalFiles.filename, ProposalFiles.path).where(proposal_id == proposal_id)
#         result = session.execute(query)

#         return result.all()
#     except Exception as ex:
#         Logger.add_to_log('error', traceback.format_exc())
#         raise ValueError("Error al obtener la contraseña.")


def get_propsal_by_id(session: Session, proposal_id: int):
    
    try:
        query = (
            select(Proposal)
            .options(
                joinedload(Proposal.proposal_user),
                joinedload(Proposal.proposal_files)
            )
            .where(Proposal.id == proposal_id)
        )
        
        result = session.execute(query)

        return result.unique().scalar_one_or_none()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


def verify_proposal_user(session: Session, user_id: int, proposal_id: int):
    try:
        query = (
            select(ProposalUsersModel)
            .where(
                and_(
                    ProposalUsersModel.proposal_id == proposal_id, 
                    ProposalUsersModel.user_id == user_id
                    )
                )
        )

        result = session.execute(query)

        return result.unique().scalar_one_or_none()
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")
    

def get_proposal_users(session: Session, proposal_id: int):
    try:
        query = (
            select(ProposalUsersModel)
            .join(ProposalUsersModel.users, isouter=True)
            .join(User.rol, isouter=True)
            .where(
                and_(ProposalUsersModel.proposal_id == proposal_id,
                    ProposalUsersModel.active == 1)))

        result = session.execute(query)

        return result.unique().scalars()
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")


def get_proposal_files(session: Session, proposal_id: int):
    try:
        query = (
            select(ProposalFiles)
            .where(
                and_(ProposalFiles.proposal_id == proposal_id,
                    ProposalFiles.active == 1)))

        result = session.execute(query)

        return result.unique().scalars()
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al comprobar la propuesta del usuario.")


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
def add_proposal_files(session: Session, proposal_files_dto: ProposalFilesDto):
    try:
        new_proposal_file = ProposalFiles(**proposal_files_dto.model_dump())

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


def inactivate_proposal(session: Session, proposal_id: int, file_id: int):
    try:
        query = (
            update(Proposal)
            .where(
                and_(Proposal.id == file_id,
                     Proposal.active == 1)))

        session.execute(query)

        session.flush()
        
        return True
    except:
        Logger.add_to_log('error', traceback.format_exc())
        return False
    

def inactivate_proposal_file(session: Session, proposal_id: int, file_id: int):
    try:
        query = (
            update(ProposalFiles)
            .where(
                and_(ProposalFiles.id == file_id,
                     ProposalFiles.proposal_id == proposal_id,
                    ProposalFiles.active == 1))
            .values(active = 0)
                    )

        session.execute(query)

        session.flush()
        return True
    except:
        Logger.add_to_log('error', traceback.format_exc())
        return False

