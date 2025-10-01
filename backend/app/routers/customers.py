from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.core.dependencies import get_current_employee, get_current_admin
from app.models.auth import UserInDB
from app.models.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.models.biometric import BiometricResponse
from app.database.supabase_client import get_supabase_client
from typing import List, Optional

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=List[CustomerResponse])
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("customers").select("*").range(skip, skip + limit - 1).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching customers: {str(e)}"
        )


@router.get("/search", response_model=List[CustomerResponse])
async def search_customers(
    query: str = Query(..., min_length=1),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("customers").select("*").or_(
            f"dni.ilike.%{query}%,first_name.ilike.%{query}%,last_name.ilike.%{query}%,email.ilike.%{query}%"
        ).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching customers: {str(e)}"
        )


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("customers").select("*").eq("id", customer_id).single().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching customer: {str(e)}"
        )


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer: CustomerCreate,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        customer_dict = customer.model_dump()
        customer_dict["status"] = customer_dict["status"].value

        if "birth_date" in customer_dict and customer_dict["birth_date"]:
            customer_dict["birth_date"] = customer_dict["birth_date"].isoformat()

        response = supabase.table("customers").insert(customer_dict).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create customer"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer with this DNI or email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating customer: {str(e)}"
        )


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_update: CustomerUpdate,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        update_dict = {k: v for k, v in customer_update.model_dump(exclude_unset=True).items() if v is not None}

        if "status" in update_dict:
            update_dict["status"] = update_dict["status"].value

        if "birth_date" in update_dict and update_dict["birth_date"]:
            update_dict["birth_date"] = update_dict["birth_date"].isoformat()

        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        response = supabase.table("customers").update(update_dict).eq("id", customer_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating customer: {str(e)}"
        )


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: str,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("customers").update({"status": "inactive"}).eq("id", customer_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting customer: {str(e)}"
        )


@router.get("/{customer_id}/biometrics", response_model=List[BiometricResponse])
async def get_customer_biometrics(
    customer_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        customer_response = supabase.table("customers").select("id").eq("id", customer_id).maybeSingle().execute()

        if not customer_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        response = supabase.table("client_biometrics").select(
            "id, client_id, type, hash_checksum, encryption_method, is_active, created_at, updated_at, meta_info"
        ).eq("client_id", customer_id).eq("is_active", True).execute()

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching customer biometrics: {str(e)}"
        )
