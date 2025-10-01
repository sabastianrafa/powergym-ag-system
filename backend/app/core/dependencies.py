from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token
from app.core.config import settings
from app.models.auth import TokenData, UserRole, UserInDB
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> UserInDB:
    if settings.DISABLE_AUTH:
        return UserInDB(
            id="fake-admin-id",
            email="admin@gym.com",
            role=UserRole.ADMIN
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception

    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    return UserInDB(
        id=token_data.user_id,
        email=token_data.email,
        role=token_data.role
    )


async def get_current_admin(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


async def get_current_employee(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if current_user.role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee or Admin privileges required"
        )
    return current_user
