from pydantic import BaseModel, Field

class GetProject(BaseModel):
    title: str = Field(None)
    priority: str = Field(None)
    status_id: int = Field(None)
    active: bool = Field(None)

class AddProject(BaseModel):
    title: str = Field(...)
    description: str = Field(...)

class UpdateProject(BaseModel):
    title: str = Field(None)
    description: str = Field(None)
    main_directory: str = Field(None)
    priority: str = Field(None)
    status_id: int = Field(None)
    active: bool = Field(None)