from pydantic import BaseModel, Field
from typing import Optional

class MimeTypeDto(BaseModel):
    mime_pattern: Optional[str] = Field(None)
    icon: Optional[str] = Field(None)
    extension: Optional[str] = Field(None)
    category_id: Optional[int] = Field(None)