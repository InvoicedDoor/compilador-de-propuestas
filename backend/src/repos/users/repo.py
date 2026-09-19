from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from src.utilities.db.db_connection import SessionLocal
from src.models.users.model import UserModel
from src.dtos.users.dto import RequesterUserDto, UserFilterDto
from src.models.company_roles.model import CompanyRoleModel
from src.models.credentials.model import Auth
from src.utilities.logger.logger import Logger
import traceback

def get_users(user: UserFilterDto):
    session = SessionLocal()
    try:
        filters = {}

        if user.id is not None:
            filters["id"] = user.id

        if user.name is not None:
            filters["name"] = user.name

        if user.first_lastname is not None:
            filters["first_lastname"] = user.first_lastname

        if user.second_lastname is not None:
            filters["second_lastname"] = user.second_lastname

        if user.rol_id is not None:
            filters["rol_id"] = user.rol_id

        if user.active is not None:
            filters["active"] = user.active



        query = (select(UserModel)
                 .filter_by(**filters)
                 .join(UserModel.role, isouter=True))

        result = session.execute(query)

        users = result.unique().scalars()

        return users.all()
    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")

    
def validate_user(user: RequesterUserDto):
    session = SessionLocal()
    try:
        query = (select(UserModel)
                 .options(
                     selectinload(UserModel.credentials)
                     .selectinload(Auth.user)
                 )
                 .where(UserModel.id == user.id
                        and Auth.mail == user.mail
                        and UserModel.rol_id == user.rol
                        and user.rol == 1))
        
        result = session.execute(query)

        users = result.unique().scalars()

        return len(users.all()) < 0
    except:
        Logger.add_to_system_log('error', traceback.format_exc())


def get_user_by_id(session: Session, user_id: int):
    try:
        query = (select(UserModel)
                 .join(UserModel.role, isouter=True)
                 .where(UserModel.id == user_id))
        
        result = session.execute(query)

        return result.unique().scalar_one_or_none()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")
    

def get_user_by_mail(session: Session, mail: str):
    try:

        query = select(Auth).where(
            Auth.mail == mail
        )

        result = session.execute(query)

        credentials = result.unique().scalar_one_or_none()

        if not credentials:
            return None

        return credentials

    except Exception as ex:

        Logger.add_to_system_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(f"Error: {ex}")

def get_bacth_user_by_mails(session: Session, mails: list[str]):

    try:

        query = select(Auth.mail,
                       Auth.user_id).where(
            Auth.mail.in_(mails)
        )

        result = session.execute(query)

        credentials = result.mappings().all()

        formated_credentials = {
            credential.mail: {
                "user_id": credential.user_id
            }
            for credential in credentials        
        } 

        return formated_credentials


    except Exception as ex:

        Logger.add_to_system_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(f"Error: {ex}")

def register_user_repo(
    session: Session,
    credentials: Auth
):

    try:
        session.add(credentials)

        session.flush()

        return True

    except Exception:

        session.rollback()

        Logger.add_to_system_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(
            "Error al agregar usuario."
        )