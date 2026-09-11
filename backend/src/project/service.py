# from .repo import get_all_project, get_project_by_id, inactivate_project, send_project, update_project
# from .dto import *
# from src.repos.project_repo import verify_project_approbation, verify_project_user
# from src.services.project_service import validate_user
# from src.utilities.files_manager.upload_files_funtion import upload_files
# from src.utilities.handlers.http_exceptions import *
# from src.utilities.logger.logger import Logger
# from src.models.user_model import RequesterUser
# from src.utilities.db.db_connection import SessionLocal
# from config import ALTERNATIVE_STATUS, APROVAL_STEPS, CLOSED_STATUS


# BACKEND_URL = "http://localhost:5000"


# def get_projects_service(user: RequesterUser, project: GetProject):
#     session = SessionLocal()
#     try:
#         project_format = []
#         if validate_user(user):
#             project_list = get_all_project(session, project)

#             if len(project_list) == 0:
#                 raise NotFound(message="No hay propuestas aún.", data=[])

#             for data in project_list:
#                 files = [{
#                     "filename": file.filename,
#                     "source": file.path
#                 } for file in data.project_files]

#                 project_format.append({
#                     "id": data.id,
#                     "title": data.title,
#                     "description": data.description,
#                     "status": {
#                         "code": data.status.status,
#                         "description": data.status.description
#                     },
#                     "source": files
#                 })

#         else:
#             project_list = get_all_user_project(session, user.id, project)
#             if len(project_list) == 0:
#                 raise NotFound(message="No hay propuestas aún.", data=[])

#             for data in project_list:
#                 files = [{
#                     "filename": file.filename,
#                     "source": file.path
#                 } for file in data.project_files]

#                 project_format.append({
#                     "id": data.id,
#                     "title": data.title,
#                     "description": data.description,
#                     "status": {
#                         "code": data.status.status,
#                         "description": data.status.description
#                     },
#                     "source": files
#                 })

#         return project_format
    
#     except DomainError as domErr:
#         raise domErr
    
#     except Exception as ex:
#         Logger.add_to_system_log("error", f"Error: {ex}")
#         session.rollback()
#         raise UnprocessableEntity("Error al procesar los archivos.") 
#     finally:
#         session.close()


# def get_project_by_id_service(user: RequesterUser, project_id: int):
#     session = SessionLocal()
#     try:
#         is_valid = verify_project_user(session, user.id, project_id)

#         if not is_valid:
#             raise BadRequest("No puedes realizar esta acción.")

#         project = get_project_by_id(session, project_id)

#         formated_project = {
#             "id": project.id,
#             "title": project.title,
#             "description": project.description,
#             "active": project.active,
#             "files": [
#             {
#                 "id": file.id,
#                 "filename": file.filename,
#                 "path": file.path
#             } for file in project.project_files]
#         }

#         return formated_project
    
#     except DomainError as domErr:
#         raise domErr
    
#     except Exception as ex:
#         Logger.add_to_system_log("error", f"Error: {ex}")
#         session.rollback()
#         raise UnprocessableEntity("Error al procesar los archivos.") 
#     finally:
#         session.close()


# def get_project_files_service(user: RequesterUser, project_id: int):
#     session = SessionLocal()
#     try:
#         is_valid = verify_project_user(session, user.id, project_id)

#         if not is_valid:
#             raise BadRequest("No puedes realizar esta acción.")

#         project_files = get_project_files(session, project_id)

#         formated_project = [{
#             "id": project_file.id,
#             "filename": project_file.filename,
#             "path": project_file.path
#         } for project_file in project_files]

#         return formated_project
    
#     except DomainError as domErr:
#         raise domErr
    
#     except Exception as ex:
#         Logger.add_to_system_log("error", f"Error: {ex}")
#         session.rollback()
#         raise UnprocessableEntity("Error al procesar la petición.") 
#     finally:
#         session.close()


# def add_project_service(new_project: AddProject, user_requester: RequesterUser):
#     session = SessionLocal()
#     try:
#         exist_project = get_all_project(session, new_project)

#         if exist_project:
#             raise Conflict("La propuesta ya existe.")

#         project_id = send_project(session, new_project)

#         if not project_id:
#             raise InternalServerError("No se pudo crear la propuesta.")

#         relation_ok = add_relation_user_project(session, user_requester.id, project_id, project_role = 1)

#         if not relation_ok:
#             raise InternalServerError("No se pudo crear la relación usuario-propuesta.")
        
#         if not project_files:
#             session.commit()
#             return "Propuesta vacía creada exitosamente."

#         results = upload_files(project_files, project_id)
        
#         if any(r is False for r in results):
#             session.rollback()
#             raise InternalServerError("Error insertando uno o más archivos.")
        
#         session.commit()
#         return "Subido correctamente."
    
#     except DomainError as domErr:
#         return domErr
    
#     except Exception as ex:
#         Logger.add_to_system_log("error", f"Error: {ex}")
#         session.rollback()
#         raise DomainError("Error al procesar los archivos.") 
    
#     finally:
#         session.close()


# def update_project_status_service(project_changes: ProjectEventDto, status: str):
#     session = SessionLocal()
#     try:
#         # Validate owner
#         is_valid = verify_project_user(session, project_changes.user_id, project_changes.project_id)

#         if not is_valid:
#             raise BadRequest("No puedes realizar esta acción.")

#         # Get project info
#         project = get_project_by_id(session, project_changes.project_id)

#         # Validate if project status wasn't cancelled, refused or finished
#         if (project.status.status in CLOSED_STATUS):
#             raise BadRequest("No se pueden actualizar los proyectos que se han terminado, cancelado o rechazado.")

#         current_step = 0

#         # Check the current project step
#         if status not in ALTERNATIVE_STATUS:
#             for step in range(len(APROVAL_STEPS)):
#                 if APROVAL_STEPS[f"STEP_{step+1}"]["status"] == project.status.status:
#                     current_step = step+1

#             # Validate correct next step
#             if status != APROVAL_STEPS[f"STEP_{current_step + 1}"]["status"]:
#                 # Verificar que corresponda al siguiente paso del flujo
#                 raise BadRequest("No puedes actualizar a este estatus.") 

#         # Validate approval desition.
#         project_approbations = verify_project_approbation(session, project.id, status)

#         print(project_approbations)

#         # Update project status.        

#         return "Proyecto actualizado."

#     except DomainError as domErr:
#         raise domErr

#     except Exception as ex:
#         Logger.add_to_system_log("error", f"Error: {ex}")
#         session.rollback()
#         raise DomainError("Error al procesar los archivos.") 
    
#     finally:
#         session.close()


# def inactive_project_status_service(project_changes: ProjectEventDto, status: bool):
#     session = SessionLocal()
#     try:
#         # Validate owner
#         is_valid = verify_project_user(session, project_changes.user_id, project_changes.project_id)

#         if not is_valid:
#             raise BadRequest("No puedes realizar esta acción.")

#         # Get project info
#         project = get_project_by_id(session, project_changes.project_id)

#         # Validate if project status wasn't cancelled, refused or finished
#         if (project.status.status in CLOSED_STATUS):
#             raise BadRequest("No se pueden actualizar los proyectos que se han terminado, cancelado o rechazado.")

#         current_step = 0

#         # Check the current project step
#         if status not in ALTERNATIVE_STATUS:
#             for step in range(len(APROVAL_STEPS)):
#                 if APROVAL_STEPS[f"STEP_{step+1}"]["status"] == project.status.status:
#                     current_step = step+1

#             # Validate correct next step
#             if status != APROVAL_STEPS[f"STEP_{current_step + 1}"]["status"]:
#                 # Verificar que corresponda al siguiente paso del flujo
#                 raise BadRequest("No puedes actualizar a este estatus.") 

#         # Validate approval desition.
#         project_approbations = verify_project_approbation(session, project.id, status)

#         print(project_approbations)

#         # Update project status.        

#         return "Proyecto actualizado."

#     except DomainError as domErr:
#         raise domErr

#     except Exception as ex:
#         Logger.add_to_system_log("error", f"Error: {ex}")
#         session.rollback()
#         raise DomainError("Error al procesar los archivos.") 
    
#     finally:
#         session.close()
