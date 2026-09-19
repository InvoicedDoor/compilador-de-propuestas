from pydantic import Field, BaseModel, model_validator
from typing import Optional

class ProjectFilesDto(BaseModel):
    project_id: int = Field(...)
    filename: str = Field(...)
    path: str = Field(...)
    code: str = Field(...)
    file_type_id: int = Field(...)

class ProjectFilesFilter(ProjectFilesDto):
    id: Optional[int] = Field(None)
    title: str = Field(None)
    description: str = Field(None)
    active: Optional[bool] = Field(None)

    @model_validator(mode="after")
    def validate_filter(self):
        if (
            not self.id and
            not self.title and
            not self.description and
            not self.active
        ):
            raise ValueError("Debes agregar un valor como filtro.")

        return self


class DeleteProjectFileDto(BaseModel):
    file_id: int = Field(...)