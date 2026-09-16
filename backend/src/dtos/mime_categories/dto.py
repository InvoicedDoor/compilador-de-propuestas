from pydantic import Field, BaseModel

class MimeCategoryDto(BaseModel):
    name: str = Field(None)