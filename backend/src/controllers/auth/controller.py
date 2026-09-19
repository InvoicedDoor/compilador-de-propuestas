from src.models.auth_model import RegisterCredentials
from src.dtos.users.dto import RequesterUserDto, UserDto
from src.dtos.auth.dto import AuthDto, ChangePasswordDto
from src.services.auth.service import auth_service, get_user_by_id_service
from src.services.credentials.service import change_password_service
from src.services.users.service import register_user
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from src.utilities.logger.logger import Logger
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
from fastapi import APIRouter, Depends, Body
import traceback

auth_routes = APIRouter()

@auth_routes.get('')
async def verify_auth(requester: RequesterUserDto = Depends(verify_authentication)):
    user_info = get_user_by_id_service(requester.id)

    return OK("Authorized", user_info).to_response()


@auth_routes.post('')
async def auth_route(
    request_body: AuthDto = Body(...)):
    try:
        payload, user_info = auth_service(request_body)

        return OK(data={"payload": payload, "user": user_info}).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()
    
    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')

@auth_routes.post("/register")
def register_route(
    user: UserDto = Body(...),
    credentials: RegisterCredentials = Body(...)):
    try:
        res_service = register_user(
            user,
            credentials
        )

        return Created(res_service).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')

# @auth_routes.post('')
# @verify_authentication
# def unauthorize_token_controller():
#     try:
#         mail = request.json['mail']
#         password = request.json['password']
#         payload, user_info = auth_service(mail, password)

#         return OK(data={"payload": payload, "user": user_info}).to_response()
    
#     except DomainError as domErr:
#         return domErr.to_dict()
    
#     except Exception as ex:
#         Logger.add_to_system_log('error', traceback.format_exc())
#         raise InternalServerError('Error')


@auth_routes.post("/change-password")
async def change_password_route(updated_credentials: ChangePasswordDto = Body(...), 
                                _: None = Depends(verify_authentication)):
    try:
        res_service = change_password_service(updated_credentials)

        return OK(res_service).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')
    