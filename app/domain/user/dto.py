import re
from typing import Optional
from pydantic import BaseModel, Field, model_validator

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

class CreateUserDto(BaseModel):
    email: str = Field(..., description="User email")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User lastname")
    password: str = Field(..., description="User password")
    phone: Optional[str] = Field(None, description="User Phonenumber")

    @model_validator(mode="before")
    @classmethod
    def validate_email(cls, data: dict) -> dict:
        if isinstance(data, dict):
            email: str = data.get("email")
            if email and not re.match(EMAIL_REGEX, email):
                raise ValueError("Invalid email address format")
        return data
