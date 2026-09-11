from src.repos.project_repo import validate_project_user
from src.utilities.db.db_connection import SessionLocal
from src.models.user_model import RequesterUser
from src.utilities.logger.logger import Logger

def test_validate_project_user_invalid_project():
    try:
        session = SessionLocal()

        user = RequesterUser(
            id=2,
            mail="donovanhdz167@gmail.com",
            rol=2
        )

        result = validate_project_user(
            session,
            user,
            1
        )

        Logger.add_to_test_log("info", f"Prueba del módulo test_validate_project_user_invalid_project(). Resultado: {result}")

        session.close()

        assert result is False

    except:
        Logger.add_to_system_log("error", "Problemas en el módulo test_project_repo, log de la función test_validate_project_user_invalid_project")