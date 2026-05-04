from src.utilities.logger.logger import Logger
from src.models.proposal_model import Proposal
from pymysql.connections import Connection
from pymysql.cursors import DictCursor
import traceback

# Función para obtener todas las propuestas.
def get_all_propsals(connection: Connection, proposal: Proposal):
    query = """
        SELECT id, title, description FROM proposal_table
        WHERE 
            (%s IS NULL OR id = %s)
            AND (%s IS NULL OR title = %s)
            AND (%s IS NULL OR description = %s)
            AND (%s IS NULL OR active = %s);
        """
    
    cursor = None
    
    try:
        cursor = connection.cursor(DictCursor)
        cursor.execute(query, (
            proposal.id, proposal.id,
            proposal.title, proposal.title,
            proposal.description, proposal.description,
            proposal.active, proposal.active
        ))

        return cursor.fetchall()

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


# Función para obtener los archivos de una propuesta.
def get_propsal_files(connection: Connection, proposal_id: int):
    query = """SELECT filename, path FROM proposal_files_table 
    WHERE proposal_id = %s;"""
    
    cursor = None
    
    try:
        cursor = connection.cursor(DictCursor)
        cursor.execute(query, (proposal_id,))

        return cursor.fetchall()
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")


# Función para obtener los datos del usuario
def get_all_user_propsal(connection: Connection):
    query = "SELECT * FROM ;"
    
    cursor = None
    
    try:
        cursor = connection.cursor(DictCursor)

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")

# Función para obtener una propuesta según su ID.
def get_propsal_by_id(connection: Connection, ):
    
    cursor = None
    
    try:
        cursor = connection.cursor(DictCursor)

    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")

# Función para agregar una propuesta.
def send_propsal(connection: Connection, title: str, description: str):
    query = "INSERT INTO proposal_table (title, description) VALUES (%s, %s);"
    
    cursor = None
    
    try:
        cursor = connection.cursor(DictCursor)
        cursor.execute(query, (title, description))

        if cursor.rowcount == 0:
            return None
        
        return cursor.lastrowid
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener propuestas.")


# Función para agregar un documento a una propuesta.
def add_proposal_files(connection: Connection, proposal_id: int, filename: str, path: str):
    query = "INSERT INTO proposal_files_table (proposal_id, filename, path) VALUES (%s, %s, %s);"
    
    cursor = None
    
    try:
        cursor = connection.cursor(DictCursor)
        cursor.execute(query, (proposal_id, filename, path))

        return cursor.rowcount > 0
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al cargar el archivo.")


def add_relation_user_proposal(connection: Connection, user_id: int, proposal_id: int):
    query = """INSERT INTO proposal_users_table (user_id, proposal_id) 
    VALUES (%s, %s);"""
    
    cursor = None
    
    try:
        cursor = connection.cursor(DictCursor)
        cursor.execute(query, (user_id, proposal_id))

        if connection.affected_rows() == 0:
            return False
        
        return True
    except Exception as ex:
        raise ValueError(f"Error: {ex}")

