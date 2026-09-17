from pydantic import Field, BaseModel, model_validator
from datetime import datetime

class CredentialDto(BaseModel):
    user_id: int = Field(...)
    mail: str = Field(...)
    password: bool = Field(...)
    last_updated: datetime = Field(...)
    active: bool = Field(...)

class CredentialFilterDto(BaseModel):
    user_id: int = Field(None)
    mail: str = Field(None)
    active: bool = Field(None)

class RegisterCredentials(BaseModel):
    mail: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)
    
    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden.")
        
        return self