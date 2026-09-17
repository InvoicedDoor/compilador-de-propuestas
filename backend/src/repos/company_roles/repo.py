from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from src.models.company_roles.model import CompanyRoleModel
from src.dtos.company_roles.dto import CompanyRoleFilter, CompanyRoleDto
from src.utilities.logger.logger import Logger
import traceback

def get_company_roles(session: Session):
    try:
        query = select(CompanyRoleModel)

        result = session.execute(query)

        company_role_list = result.unique().scalars()

        return company_role_list.all()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al autenticarse.")

def get_company_role_by_id_or_code(session: Session, role_filter: CompanyRoleFilter):
    filters = {}
    try:
        query = (select(CompanyRoleModel)
            .filter_by(**role_filter))

        result = session.execute(query)

        company_role_list = result.unique().scalars()

        return company_role_list.all()
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al autenticarse.")

def add_company_role(session: Session, new_role: CompanyRoleModel):
    try:
        
        session.add(new_role)

        session.flush()

        return True
    except:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise ValueError("Error al agregar un rol en la compañía.")