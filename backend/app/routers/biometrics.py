from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from app.core.dependencies import get_current_employee, get_current_admin
from app.models.auth import UserInDB
from app.models.biometric import BiometricResponse
from app.database.supabase_client import get_supabase_client
from typing import List, Optional
import base64
import hashlib

router = APIRouter(prefix="/biometrics", tags=["Biometrics"])


@router.get("", response_model=List[BiometricResponse])
async def list_biometrics(
    client_id: Optional[str] = None,
    biometric_type: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        query = supabase.table("client_biometrics").select(
            "id, client_id, type, hash_checksum, encryption_method, is_active, created_at, updated_at, meta_info"
        )

        if client_id:
            query = query.eq("client_id", client_id)

        if biometric_type:
            query = query.eq("type", biometric_type)

        response = query.eq("is_active", True).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching biometrics: {str(e)}"
        )


@router.get("/{biometric_id}", response_model=BiometricResponse)
async def get_biometric(
    biometric_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("client_biometrics").select(
            "id, client_id, type, hash_checksum, encryption_method, is_active, created_at, updated_at, meta_info"
        ).eq("id", biometric_id).maybeSingle().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Biometric data not found"
            )

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching biometric: {str(e)}"
        )


@router.post("", response_model=BiometricResponse, status_code=status.HTTP_201_CREATED)
async def create_biometric(
    client_id: str = Form(...),
    biometric_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        customer_response = supabase.table("customers").select("id").eq("id", client_id).maybeSingle().execute()

        if not customer_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        if biometric_type not in ["face", "fingerprint"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid biometric type. Must be 'face' or 'fingerprint'"
            )

        file_content = await file.read()

        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size must be less than 10MB"
            )

        hash_checksum = hashlib.sha256(file_content).hexdigest()

        biometric_data = {
            "client_id": client_id,
            "type": biometric_type,
            "data": base64.b64encode(file_content).decode('utf-8'),
            "hash_checksum": hash_checksum,
            "is_active": True
        }

        response = supabase.table("client_biometrics").insert(biometric_data).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create biometric data"
            )

        biometric_response = supabase.table("client_biometrics").select(
            "id, client_id, type, hash_checksum, encryption_method, is_active, created_at, updated_at, meta_info"
        ).eq("id", response.data[0]["id"]).maybeSingle().execute()

        return biometric_response.data
    except HTTPException:
        raise
    except Exception as e:
        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Biometric data of type '{biometric_type}' already exists for this customer"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating biometric data: {str(e)}"
        )


@router.put("/{biometric_id}", response_model=BiometricResponse)
async def update_biometric(
    biometric_id: str,
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        existing = supabase.table("client_biometrics").select("id, client_id, type").eq("id", biometric_id).maybeSingle().execute()

        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Biometric data not found"
            )

        file_content = await file.read()

        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size must be less than 10MB"
            )

        hash_checksum = hashlib.sha256(file_content).hexdigest()

        update_data = {
            "data": base64.b64encode(file_content).decode('utf-8'),
            "hash_checksum": hash_checksum
        }

        response = supabase.table("client_biometrics").update(update_data).eq("id", biometric_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Biometric data not found"
            )

        biometric_response = supabase.table("client_biometrics").select(
            "id, client_id, type, hash_checksum, encryption_method, is_active, created_at, updated_at, meta_info"
        ).eq("id", biometric_id).maybeSingle().execute()

        return biometric_response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating biometric data: {str(e)}"
        )


@router.delete("/{biometric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_biometric(
    biometric_id: str,
    current_user: UserInDB = Depends(get_current_admin)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("client_biometrics").update({"is_active": False}).eq("id", biometric_id).execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Biometric data not found"
            )

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting biometric data: {str(e)}"
        )


@router.get("/{biometric_id}/data")
async def get_biometric_data(
    biometric_id: str,
    current_user: UserInDB = Depends(get_current_employee)
):
    supabase = get_supabase_client()

    try:
        response = supabase.table("client_biometrics").select(
            "id, client_id, type, data, hash_checksum"
        ).eq("id", biometric_id).eq("is_active", True).maybeSingle().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Biometric data not found"
            )

        return {
            "id": response.data["id"],
            "client_id": response.data["client_id"],
            "type": response.data["type"],
            "data": response.data["data"],
            "hash_checksum": response.data["hash_checksum"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching biometric data: {str(e)}"
        )
