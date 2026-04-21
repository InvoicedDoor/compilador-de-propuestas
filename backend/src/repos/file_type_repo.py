from src.utilities.db.db_connection import connect_to_database
from src.utilities.logger.logger import Logger
import traceback

def get_file_types_repo():
    connection = connect_to_database()
    connection.connect_timeout = 900
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM file_types_table;"

        cursor.execute(query)

        return cursor.fetchall()
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
