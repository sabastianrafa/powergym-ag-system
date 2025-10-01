from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.dependencies import get_current_employee, get_current_admin
from app.models.auth import UserInDB
from app.models.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.database.supabase_client import get_supabase_client
from typing import List, Optional

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("", response_model=List[PaymentResponse])
async def list_payments(
    customer_id: Optional[str] = Query(None),
    subscription_id: Optional[str] = Query(None),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        query = supabase.table("payments").select("*")

        if customer_id:
            query = query.eq("customer_id", customer_id)

        if subscription_id:
            query = query.eq("subscription_id", subscription_id)

        response = query.order("payment_date", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching payments: {str(e)}"
        )


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("payments").select("*").eq("id", payment_id).single().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching payment: {str(e)}"
        )


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        payment_dict = payment.model_dump()
        payment_dict["amount"] = float(payment_dict["amount"])
        payment_dict["payment_method"] = payment_dict["payment_method"].value
        payment_dict["status"] = payment_dict["status"].value

        response = supabase.table("payments").insert(payment_dict).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create payment"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating payment: {str(e)}"
        )


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: str,
    payment_update: PaymentUpdate,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        update_dict = {k: v for k, v in payment_update.model_dump(exclude_unset=True).items() if v is not None}

        if "status" in update_dict:
            update_dict["status"] = update_dict["status"].value

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        response = supabase.table("payments").update(update_dict).eq("id", payment_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating payment: {str(e)}"
        )


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: str,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("payments").delete().eq("id", payment_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting payment: {str(e)}"
        )
