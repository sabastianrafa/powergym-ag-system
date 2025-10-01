from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user, get_current_admin, get_current_employee
from app.models.auth import UserInDB

router = APIRouter(prefix="/protected", tags=["Protected Test Routes"])


@router.get("/admin")
async def admin_only_route(current_user: UserInDB = Depends(get_current_admin)):
    return {
        "message": "Admin access granted",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role
        }
    }


@router.get("/employee")
async def employee_route(current_user: UserInDB = Depends(get_current_employee)):
    return {
        "message": "Employee access granted",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role
        }
    }


@router.get("/me")
async def get_current_user_info(current_user: UserInDB = Depends(get_current_user)):
    return {
        "message": "Authenticated user information",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role
        }
    }
