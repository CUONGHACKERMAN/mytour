import jwt
import uuid
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from .auth import AuthorizationContext

BLACKLISTED_TOKENS: dict[str, float] = {}

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
        payload['jti'] = str(uuid.uuid4())
        payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=self.__jwt_config.access_token_expire)
        return jwt.encode(payload, self.__jwt_config.secret, algorithm=self.__jwt_config.algorithm)

    def verify_jwt_token(self, token: str) -> AuthorizationContext:
        try:
            payload = jwt.decode(token, self.__jwt_config.secret, algorithms=[self.__jwt_config.algorithm])
            jti = payload.get("jti")
            exp = payload.get("exp")
            if jti and exp and exp > datetime.now(timezone.utc).timestamp():
                if jti in BLACKLISTED_TOKENS:
                    raise jwt.InvalidTokenError("Token has been revoked")
            return AuthorizationContext.model_validate(payload)
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError as err:
            raise Exception(str(err) if str(err) else "Invalid token")

    def invalid_jwt_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, self.__jwt_config.secret, algorithms=[self.__jwt_config.algorithm])
            jti = payload.get("jti")
            exp = payload.get("exp")
            if jti and exp:
                BLACKLISTED_TOKENS[jti] = exp
                self._cleanup_expired_tokens()
                return True
            return False
        except jwt.InvalidTokenError:
            return False

    def _cleanup_expired_tokens(self):
        now = datetime.now(timezone.utc).timestamp()

        expired = [jti for jti, exp in BLACKLISTED_TOKENS.items() if exp <= now]
        for jti in expired:
            del BLACKLISTED_TOKENS[jti]


