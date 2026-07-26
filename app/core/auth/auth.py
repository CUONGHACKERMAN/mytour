from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AuthorizationContext(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    iat: Optional[datetime] = None
    exp: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
