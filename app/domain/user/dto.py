import re
from typing import Optional
from pydantic import BaseModel, Field, model_validator

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def validate_email(data: dict) -> dict:
    if isinstance(data, dict):
        email: str = data.get("email")
        if email and not re.match(EMAIL_REGEX, email):
            raise ValueError("Invalid email address format")
    return data

class CreateUserDto(BaseModel):
    email: str = Field(..., description="User email")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User lastname")
    password: str = Field(..., description="User password")
    phone: Optional[str] = Field(None, description="User Phonenumber")

    @model_validator(mode="before")
    @classmethod
    def email_validator(cls, data: dict) -> dict:
        validate_email(data)
        return data

class UpdateUserDto(BaseModel):
    email: Optional[str] = Field(None, description="User email")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User lastname")
    password: Optional[str] = Field(None, description="User password")
    phone: Optional[str] = Field(None, description="User Phonenumber")

    @model_validator(mode="before")
    @classmethod
    def email_validator(cls, data: dict) -> dict:
        validate_email(data)
        return data