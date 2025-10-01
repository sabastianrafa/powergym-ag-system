from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.dependencies import get_current_employee, get_current_admin
from app.models.auth import UserInDB
from app.models.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.database.supabase_client import get_supabase_client
from typing import List, Optional
from datetime import timedelta

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.get("", response_model=List[SubscriptionResponse])
async def list_subscriptions(
    customer_id: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        query = supabase.table("subscriptions").select("*")

        if customer_id:
            query = query.eq("customer_id", customer_id)

        if status_filter:
            query = query.eq("status", status_filter)

        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching subscriptions: {str(e)}"
        )


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("subscriptions").select("*").eq("id", subscription_id).single().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching subscription: {str(e)}"
        )


@router.post("", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription: SubscriptionCreate,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        active_subs = supabase.table("subscriptions").select("*").eq(
            "customer_id", subscription.customer_id
        ).eq("status", "active").execute()

        if active_subs.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer already has an active subscription"
            )

        plan_response = supabase.table("plans").select("duration_days").eq("id", subscription.plan_id).single().execute()

        if not plan_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found"
            )

        duration_days = plan_response.data["duration_days"]
        end_date = subscription.start_date + timedelta(days=duration_days)

        subscription_dict = subscription.model_dump()
        subscription_dict["end_date"] = end_date.isoformat()
        subscription_dict["start_date"] = subscription_dict["start_date"].isoformat()
        subscription_dict["status"] = "active"

        response = supabase.table("subscriptions").insert(subscription_dict).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create subscription"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating subscription: {str(e)}"
        )


@router.put("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: str,
    subscription_update: SubscriptionUpdate,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        update_dict = {k: v for k, v in subscription_update.model_dump(exclude_unset=True).items() if v is not None}

        if "status" in update_dict:
            update_dict["status"] = update_dict["status"].value

        if "end_date" in update_dict:
            update_dict["end_date"] = update_dict["end_date"].isoformat()

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        response = supabase.table("subscriptions").update(update_dict).eq("id", subscription_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating subscription: {str(e)}"
        )


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_subscription(
    subscription_id: str,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("subscriptions").update({"status": "cancelled"}).eq("id", subscription_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cancelling subscription: {str(e)}"
        )
