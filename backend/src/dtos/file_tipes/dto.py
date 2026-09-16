from pydantic import Field, BaseModel

class FileTypeDto(BaseModel):
    description: str = Field(None)
    is_main_image: bool = Field(None)
    mime_type_id: int = Field(None)
    active: bool = Field(None)