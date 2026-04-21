from src.utilities.db.db_connection import connect_to_database
from src.utilities.hashing.hashing_password import password_encryption, validate_password
from src.models.user_model import User, RegisterUser
from src.models.auth_model import Auth, RegisterCredentials, GetAuth
from src.utilities.logger.logger import Logger
from pymysql.cursors import DictCursor
import traceback

def get_hashed_password(mail: str):
    connection = connect_to_database()
    connection.connect_timeout = 900
    try:
        cursor = connection.cursor()
        query = "SELECT password FROM users_table WHERE mail = %s;"

        cursor.execute(query, (mail,))

        return cursor.fetchone()
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al obtener la contraseña.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_auth(mail: str):
    connection = connect_to_database()
    connection.connect_timeout = 900

    try:
        cursor = connection.cursor(DictCursor)
        cursor.callproc("get_auth", (mail,))
        row = cursor.fetchone()
        cursor.nextset()

        if not row:
            return None

        return GetAuth(**row)
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al autenticarse.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def change_password(mail, new_password):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = "UPDATE credentials_table SET password = %s WHERE mail = %s"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (new_password, mail))

        if connection.affected_rows() == 0:
            return False
        
        connection.commit()
        return True
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
def get_user_by_mail(mail: str):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = "SELECT * FROM credentials_table WHERE mail = %s;"
    try:
        cursor = connection.cursor(DictCursor)
        cursor.execute(query, (mail,))

        if cursor.rowcount == 0:
            return None
        
        credentials = cursor.fetchone()
        return GetAuth(**credentials)
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError(f"Error: {ex}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
def register_user(user: RegisterUser, credentials: RegisterCredentials):
    connection = connect_to_database()
    connection.connect_timeout = 900
    try:
        cursor = connection.cursor()
        new_user: User = cursor.callproc("register_user", (user.name, user.rol_id))

        if not new_user:
            return False

        new_credentials: Auth = cursor.callproc("register_credentials", (credentials.user_id))

        if not new_credentials:
            return False
        
        connection.commit()
        return True
    except:
        Logger.add_to_log('error', traceback.format_exc())
        raise ValueError("Error al agregar al usuario.")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()