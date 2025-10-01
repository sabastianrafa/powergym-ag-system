from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.dependencies import get_current_employee, get_current_admin
from app.models.auth import UserInDB
from app.models.attendance import AttendanceCreate, AttendanceResponse
from app.database.supabase_client import get_supabase_client
from typing import List, Optional
from datetime import date, datetime, time

router = APIRouter(prefix="/attendances", tags=["Attendances"])


@router.get("", response_model=List[AttendanceResponse])
async def list_attendances(
    customer_id: Optional[str] = Query(None),
    date_filter: Optional[date] = Query(None),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        query = supabase.table("attendances").select("*")

        if customer_id:
            query = query.eq("customer_id", customer_id)

        if date_filter:
            start_datetime = datetime.combine(date_filter, time.min)
            end_datetime = datetime.combine(date_filter, time.max)
            query = query.gte("check_in_time", start_datetime.isoformat()).lte("check_in_time", end_datetime.isoformat())

        response = query.order("check_in_time", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendances: {str(e)}"
        )


@router.get("/today", response_model=List[AttendanceResponse])
async def get_today_attendances(
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        today = date.today()
        start_datetime = datetime.combine(today, time.min)
        end_datetime = datetime.combine(today, time.max)

        response = supabase.table("attendances").select("*").gte(
            "check_in_time", start_datetime.isoformat()
        ).lte(
            "check_in_time", end_datetime.isoformat()
        ).order("check_in_time", desc=True).execute()

        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching today's attendances: {str(e)}"
        )


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def create_attendance(
    attendance: AttendanceCreate,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        today = date.today()

        active_subscription = supabase.table("subscriptions").select("*").eq(
            "customer_id", attendance.customer_id
        ).eq("status", "active").gte("end_date", today.isoformat()).execute()

        if not active_subscription.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer does not have an active subscription"
            )

        attendance_dict = attendance.model_dump()

        response = supabase.table("attendances").insert(attendance_dict).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create attendance"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating attendance: {str(e)}"
        )


@router.get("/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance(
    attendance_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("attendances").select("*").eq("id", attendance_id).single().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance not found"
            )

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching attendance: {str(e)}"
        )


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    attendance_id: str,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("attendances").delete().eq("id", attendance_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance not found"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting attendance: {str(e)}"
        )
