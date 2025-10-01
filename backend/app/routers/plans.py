from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.dependencies import get_current_employee, get_current_admin
from app.models.auth import UserInDB
from app.models.plan import PlanCreate, PlanUpdate, PlanResponse
from app.database.supabase_client import get_supabase_client
from typing import List

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("", response_model=List[PlanResponse])
async def list_plans(
    active_only: bool = Query(False),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        query = supabase.table("plans").select("*")

        if active_only:
            query = query.eq("is_active", True)

        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching plans: {str(e)}"
        )


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("plans").select("*").eq("id", plan_id).single().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found"
            )

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching plan: {str(e)}"
        )


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def create_plan(
    plan: PlanCreate,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        plan_dict = plan.model_dump()
        plan_dict["price"] = float(plan_dict["price"])

        response = supabase.table("plans").insert(plan_dict).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create plan"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating plan: {str(e)}"
        )


@router.put("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: str,
    plan_update: PlanUpdate,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        update_dict = {k: v for k, v in plan_update.model_dump(exclude_unset=True).items() if v is not None}

        if "price" in update_dict:
            update_dict["price"] = float(update_dict["price"])

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        response = supabase.table("plans").update(update_dict).eq("id", plan_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating plan: {str(e)}"
        )


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(
    plan_id: str,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("plans").update({"is_active": False}).eq("id", plan_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting plan: {str(e)}"
        )
