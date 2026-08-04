# app/domain/auth/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from typing import Optional
from core.auth import AuthorizationContext
from .service import AuthService


def get_auth_service() -> AuthService:
    return AuthService()

async def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
) -> AuthorizationContext:
    token = request.cookies.get("id_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return auth_service.verify_jwt_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
