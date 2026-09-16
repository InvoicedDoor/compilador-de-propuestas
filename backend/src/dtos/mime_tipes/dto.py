from pydantic import Field, BaseModel
from typing import Optional

class MimeTypeDto(BaseModel):
    mime_pattern: Optional[str] = Field(None)
    icon: Optional[str] = Field(None)
    extension: Optional[str] = Field(None)
    category_id: Optional[int] = Field(None)