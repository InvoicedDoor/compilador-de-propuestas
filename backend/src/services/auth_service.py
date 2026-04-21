from ..repos.auth_repo import get_auth, change_password, get_user_by_mail
from ..repos.user_repo import get_user_by_id
from src.utilities.hashing.hashing_password import validate_password, password_encryption
from src.utilities.db.db_connection import connect_to_database
from src.utilities.logger.logger import Logger
from config import Config
from flask import jsonify
from traceback import format_exc
from jwt import encode
from datetime import (
    datetime, 
    timedelta)

key = Config.SECRET_KEY

def auth_service(mail: str, password: str):

    try:
        credentials = get_auth(mail)

        if not credentials:
            return jsonify({
                "message": "El usuario no existe.",
                "data": {}
            }), 403

        valid_password = validate_password(password, credentials.password)

        if not valid_password:
            return jsonify({
                "message": "La contraseña es incorrecta.",
                "data": {}
            }), 403
        
        user = get_user_by_id(credentials.user_id)

        if not user:
            return jsonify({
                "message": "El usuario no tiene registro.",
                "data": {}
            }), 409

        payload = {
            'id': user.id,
            'name': user.name,
            'mail': credentials.mail,
            'rol': user.rol_id,
            'exp': datetime.utcnow() + timedelta(minutes=120)
        }

        return jsonify({
            "data": encode(payload, key, algorithm='HS256'),
            "message": "Inicio de sesión correcto.",
        })
                
    except Exception as ex:
        Logger.add_to_log('error', format_exc())
        return jsonify({
            "message": "Error",
            "data": {}
        }), 500

def change_password_service(mail: str, old_password: str = None, new_password: str = None, new_password_confirmation: str = None):
    
    if new_password != new_password_confirmation:
        return jsonify({
                "data": {},
                "message": "La contraseña no coincide con la confirmación."
            }), 409

    try:
        credentials = get_user_by_mail(mail)
        if not credentials:
            return jsonify({
                "data": {},
                "message": "El correo no está registrado."
            }), 401
        
        is_valid = validate_password(old_password, credentials.password)

        if not is_valid:
            return jsonify({
                "data": {},
                "message": "No capturaste la contraseña correcta. No puedes cambiar la contraseña sin las credenciales correctas."
            }), 409
        
        hashed_password = password_encryption(new_password)
        is_changed = change_password(mail, hashed_password)
        if not is_changed:
            return jsonify({
                "data": {},
                "message": "No se pudo cambiar la contraseña."
            }), 409
        
        return jsonify({
            "message": "Contraseña modificada con éxito.",
            "data": {}
        }), 201
    except:
        Logger.add_to_log('error', format_exc())
        return jsonify({
            "data": {},
            "message": "Error en el servidor."
        }), 500

def register_user(name, mail, password, rol):
    connection = connect_to_database()
    connection.connect_timeout = 900
    query = 'SELECT * FROM system_users WHERE mail = %s'
    insertion = 'INSERT INTO system_users (name, mail, password, salt, rol) \
    VALUES (%s, %s, %s, %s, %s)'
    try:
        cursor = connection.cursor()
        cursor.execute(query, mail)
        user = cursor.fetchone()
        
        if user:
            return jsonify("El usuario está registrado."), 409
        
        newPassword, salt = password_encryption(password)
        
        cursor.execute(insertion, [name, mail, newPassword, salt, rol])
        connection.commit()
        
        if cursor.rowcount == 1:
            return jsonify("Registro realizado.")
        
        return jsonify('No se pudo realizar el registro.'), 500
    except Exception as ex:
        Logger.add_to_log('error', format_exc())
        return "Error", 500
    finally:
        if cursor:
            cursor.close()
        connection.close()