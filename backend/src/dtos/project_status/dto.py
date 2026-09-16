from pydantic import Field, BaseModel
from typing import Optional

class UpdateProjectStatusBody(BaseModel):
    status: str