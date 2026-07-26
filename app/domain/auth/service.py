from . import JwtAuthService, hash_password, verify_password, AuthorizationContext
from core.config import settings

class AuthService:
    def __init__(self):
        self.__jwt_service = JwtAuthService(
            secret= settings.JWT_SECRET,
            algorithm= settings.JWT_ALGORITHM,
            access_token_expire= settings.JWT_ACCESS_TOKEN_EXPIRE,
        )

    def verify_password(self, plain_password: str, hashed_password: str):
        return verify_password(plain_password, hashed_password)

    def hash_password(self, password: str):
        return hash_password(password)

    def create_user_session(self, user):
        context = AuthorizationContext(
            id=str(user.get('id')),
            email=user.get('email'),
            first_name=user.get('first_name'),
            last_name=user.get('last_name'),
            phone=user.get('phone')
        )
        return self.__jwt_service.create_jwt_token(context)
