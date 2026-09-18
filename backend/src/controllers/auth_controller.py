from ..services.auth_service import auth_service, change_password_service, get_user_by_id_service
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from fastapi import Request, APIRouter, Depends
from src.utilities.logger.logger import Logger
from src.utilities.handlers.http_exceptions import *
from src.utilities.handlers.http_success import *
import traceback

auth_routes = APIRouter()

@auth_routes.get('')
async def verify_auth(request: Request, _: None = Depends(verify_authentication)):
    requester_info = request.state.user
    user_info = get_user_by_id_service(requester_info["id"])

    return OK("Authorized", user_info).to_response()


@auth_routes.post('')
async def auth_route(request: Request):
    try:
        request_body = await request.json()
        mail = request_body['mail']
        password = request_body['password']
        payload, user_info = auth_service(mail, password)

        return OK(data={"payload": payload, "user": user_info}).to_response()
    
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
async def change_password_route(request: Request):
    try:
        request_body = await request.json()
        mail = request_body["mail"]
        old_password = request_body['old_password']
        new_password = request_body['new_password']
        new_password_confirmation = request_body['new_password_confirmation']

        res_service = change_password_service(mail, old_password, new_password, new_password_confirmation)

        return OK(res_service).to_response()
    
    except DomainError as domErr:
        return domErr.to_dict()

    except Exception as ex:
        Logger.add_to_system_log('error', traceback.format_exc())
        raise InternalServerError('Error')
    