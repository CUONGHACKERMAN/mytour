from pydantic import BaseModel
from typing import Optional

class SignInDto(BaseModel):
    email: str
    password: str

class SignUpDto(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
