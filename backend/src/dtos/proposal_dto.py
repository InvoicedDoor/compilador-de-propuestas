from pydantic import Field, BaseModel

class ProposalDto(BaseModel):
    proposal_title: str = Field(...)
    proposal_description: str = Field(...)
    proposal_manager: int = Field(...)
