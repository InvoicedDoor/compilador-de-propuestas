from pydantic import Field, BaseModel
from typing import Optional

class Proposal(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    active: Optional[bool] = None

class ProposalFilter(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None