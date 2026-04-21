from src.utilities.db.db_connection import connect_to_database
from src.utilities.logger.logger import Logger
from src.models.proposal_model import Proposal
from pymysql.cursors import DictCursor
import traceback


# Función para obtener todas las propuestas.
def get_all_propsals(proposal: Proposal):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = """
        SELECT id, title, description FROM proposal_table
        WHERE 
            (%s IS NULL OR id = %s)
            AND (%s IS NULL OR title = %s)
            AND (%s IS NULL OR description = %s)
            AND (%s IS NULL OR active = %s);
        """
    try:
        cursor = connection.cursor()
        cursor.execute(query, (
            proposal.id, proposal.id,
            proposal.title, proposal.title,
            proposal.description, proposal.description,
            proposal.active, proposal.active
        ))

        return cursor.fetchall()

    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Función para obtener los archivos de una propuesta.
def get_propsal_files(proposal_id: int):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = """SELECT filename, path FROM proposal_files_table 
    WHERE proposal_id = %s;"""
    try:
        cursor = connection.cursor()
        cursor.execute(query, (proposal_id))

        return cursor.fetchall()
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Función para obtener los datos del usuario
def get_all_user_propsal():
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = "SELECT * FROM ;"
    try:
        cursor = connection.cursor()

    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Función para obtener una propuesta según su ID.
def get_propsal_by_id():
    connection = connect_to_database()
    connection.connect_timeout = 900
    try:
        cursor = connection.cursor()

    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Función para agregar una propuesta.
def send_propsal(title: str, description: str):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = "INSERT INTO proposal_table (title, description) VALUES (%s, %s);"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (title, description))

        if connection.affected_rows() == 0:
            return None
        
        connection.commit()

        # Retorna el id del nuevo registro.
        return cursor.lastrowid
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Función para agregar un documento a una propuesta.
def add_proposal_files(proposal_id: int, filename: str, path: str):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = "INSERT INTO proposal_files_table (proposal_id, filename, path) VALUES (%s, %s, %s);"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (proposal_id, filename, path))
        connection.commit()

        return cursor.rowcount > 0
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al cargar el archivo.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def add_relation_user_proposal(user_id: int, proposal_id: int):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = """INSERT INTO proposal_users_table (user_id, proposal_id) 
    VALUES (%s, %s);"""
    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, proposal_id))

        if connection.affected_rows() == 0:
            return False
        
        connection.commit()
        return True
    except Exception as ex:
        raise ValueError(f"Error: {ex}")
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()

