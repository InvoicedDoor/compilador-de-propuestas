from flask import request, jsonify
import functools
import jwt
import os
from dotenv import load_dotenv
from traceback import format_exc
from src.utilities.logger.logger import Logger

load_dotenv()

key = os.getenv("SECRET_KEY")


def verify_authentication(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Authorization header missing"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Invalid token format"}), 401

        token = auth_header.split(" ")[1]

        try:
            decoded_token = jwt.decode(token, key, algorithms=["HS256"])
            request.user = decoded_token  # opcional: guardar payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401
        except Exception:
            Logger.add_to_log("error", format_exc())
            return jsonify({"message": "Authentication error"}), 401

        return func(*args, **kwargs)

    return wrapper