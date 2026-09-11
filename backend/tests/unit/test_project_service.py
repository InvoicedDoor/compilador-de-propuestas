from types import SimpleNamespace
from unittest.mock import ANY, patch

from src.services.project_service import get_projects_service


@patch("src.services.project_service.validate_user")
@patch("src.services.project_service.get_all_project")
def test_get_projects_authorized_user(
    mock_get_all_project,
    mock_validate_user
):
    # Arrange
    user = SimpleNamespace(id=10)
    project_filter = SimpleNamespace()

    mock_validate_user.return_value = True

    file = SimpleNamespace(filename="manual.pdf", path="/files/manual.pdf")

    status = SimpleNamespace(
        status="ACTIVE",
        description="Proyecto activo"
    )

    project_data = SimpleNamespace(
        id=1,
        title="Proyecto de prueba",
        description="Descripción de prueba",
        status=status,
        project_files=[file]
    )

    mock_get_all_project.return_value = [project_data]

    # Act
    result = get_projects_service(user, project_filter)

    # Assert
    assert result == [
        {
            "id": 1,
            "title": "Proyecto de prueba",
            "description": "Descripción de prueba",
            "status": {
                "code": "ACTIVE",
                "description": "Proyecto activo"
            },
            "source": [
                {
                    "filename": "manual.pdf",
                    "source": "/files/manual.pdf"
                }
            ]
        }
    ]

    mock_validate_user.assert_called_once_with(user)

    mock_get_all_project.assert_called_once_with(
        ANY,
        project_filter
    )