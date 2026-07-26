import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from .auth import AuthorizationContext

class JwtConfig(BaseModel):
    secret: str
    algorithm: str
    access_token_expire: int = 60

class JwtAuthService:
    def __init__(self, **kwargs):
        self.__jwt_config = JwtConfig(**kwargs)

    def create_jwt_token(self, context: AuthorizationContext) -> str:
        payload = context.model_dump()
        payload['iat'] = datetime.now(timezone.utc)
        payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=self.__jwt_config.access_token_expire)
        return jwt.encode(payload, self.__jwt_config.secret, algorithm=self.__jwt_config.algorithm)

    def verify_jwt_token(self, token: str) -> AuthorizationContext:
        try:
            payload = jwt.decode(token, self.__jwt_config.secret, algorithms=[self.__jwt_config.algorithm])
            return AuthorizationContext.model_validate(payload)
        except jwt.ExpiredSignatureError as err:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError as err:
            raise Exception("Invalid token")
