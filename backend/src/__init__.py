from fastapi import APIRouter
from src.controllers.auth_controller import auth_routes

main_router = APIRouter()

main_router.include_router(auth_routes, prefix="/auth")
# main_router.include_router(user_router)
# main_router.include_router(questionary_router)
# main_router.include_router(msg_router)
# main_router.include_router(files_router)