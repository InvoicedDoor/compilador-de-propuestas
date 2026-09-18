from fastapi.requests import Request
from fastapi import HTTPException
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("SECRET_KEY")

async def verify_authentication(request: Request):

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )

    token = auth_header.split(" ", 1)[1]

    try:
        decoded_token = jwt.decode(
            token,
            key,
            algorithms=["HS256"]
        )

        request.state.user = decoded_token

        return decoded_token

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expirado"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )