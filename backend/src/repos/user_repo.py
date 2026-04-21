from src.utilities.db.db_connection import connect_to_database
from src.models.user_model import RowUser
from src.utilities.logger.logger import Logger
from pymysql.cursors import DictCursor
import traceback

def get_users():
    try:
        pass
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")

def get_user_by_id(user_id: int):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = "SELECT * FROM users_table WHERE id = %s;"
    try:
        cursor = connection.cursor(DictCursor)
        cursor.execute(query, (user_id,))
        
        if cursor.rowcount == 0:
            return None
        
        user = cursor.fetchone()

        return RowUser(**user)
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")
