from pydantic import BaseModel, Field

class Rol(BaseModel):
    id: int = Field(...)
    rol: str = Field(...)