from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from core.auth import AuthorizationContext
from domain.user import UserService, get_user_service
from .service import AuthService
from .dependency import get_auth_service, get_current_user, security
from .dto import SignInDto, SignUpDto

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/sign-in",
    status_code=status.HTTP_200_OK
)
async def sign_in(
    payload: SignInDto,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    ## Find user
    user = await user_service.find_user_by_email(payload.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    ## Verify credentials
    if not auth_service.verify_password(payload.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    ## Token grant
    token = auth_service.create_user_session(user)

    return {"access_token": token, "token_type": "bearer"}

@router.post(
    "/sign-out",
    status_code=status.HTTP_200_OK
)
async def sign_out(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    context: AuthorizationContext = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = credentials.credentials
    auth_service.invalidate_user_session(token)
    return {"message": "User signed out successfully"}

@router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED
)
async def sign_up(
    payload: SignUpDto,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    ## Find user by email
    user = await user_service.find_user_by_email(payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )


    ## Create User
    password = auth_service.hash_password(payload.password)

    new_user = await user_service.create_user({
        "email": payload.email,
        "password": password,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "phone": payload.phone
    })

    return {"message": "User created successfully"}
