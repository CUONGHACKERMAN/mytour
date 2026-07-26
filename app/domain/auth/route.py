from fastapi import APIRouter, Depends, HTTPException, status
from domain.user import UserService, get_user_service
from .service import AuthService
from .dto import SignInDto, SignUpDto

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_auth_service() -> AuthService:
    return AuthService()

@router.post(
    "/sign-in",
    status_code=status.HTTP_200_OK
)
async def sign_in(
    payload: SignInDto,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await user_service.find_user_by_email(payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not auth_service.verify_password(payload.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = auth_service.create_user_session(user)
    return {"access_token": token, "token_type": "bearer"}

@router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED
)
async def sign_up(
    payload: SignUpDto,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await user_service.find_user_by_email(payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    password = auth_service.hash_password(payload.password)

    new_user = await user_service.create_user({
        "email": payload.email,
        "password": password,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "phone": payload.phone
    })

    return {"message": "User created successfully"}
