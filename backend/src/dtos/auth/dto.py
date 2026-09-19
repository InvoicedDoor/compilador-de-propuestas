from pydantic import BaseModel

class AuthDto(BaseModel):
    mail: str
    password: str

class ChangePasswordDto(BaseModel):
    mail: str
    old_password: str
    new_password: str
    new_password_confirmation: str