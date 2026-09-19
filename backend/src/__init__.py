from fastapi import APIRouter
from .controllers.auth.controller import auth_routes
from .controllers.project_events.controller import project_events_routes
from .controllers.project_files.controller import project_files_routes
from .controllers.project_roles.controller import project_roles_routes
from .controllers.project_status.controller import project_status_routes
from .controllers.project_users.controller import project_users_routes
from .controllers.projects.controller import projects_routes

main_router = APIRouter()

main_router.include_router(auth_routes, prefix="/auth")
main_router.include_router(projects_routes, prefix="/projects")
main_router.include_router(project_events_routes, prefix="/project-events")
main_router.include_router(project_files_routes, prefix="/project-files")
main_router.include_router(project_roles_routes, prefix="/project-roles")
main_router.include_router(project_status_routes, prefix="/project-status")
main_router.include_router(project_users_routes, prefix="/project-users")
# main_router.include_router(user_router)
# main_router.include_router(questionary_router)
# main_router.include_router(msg_router)
# main_router.include_router(files_router)