from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class BiometricType(str, Enum):
    FACE = "face"  # reconocimiento facial
    FINGERPRINT = "fingerprint"  # reconocimiento por huella dactilar


class BiometricBase(BaseModel):
    client_id: str
    type: BiometricType
    data: bytes
    compressed_data: Optional[bytes] = None
    thumbnail: Optional[bytes] = None
    embedding: Optional[List[float]] = None
    hash_checksum: Optional[str] = None
    encryption_method: Optional[str] = None
    is_active: bool = True
    meta_info: Optional[Dict[str, Any]] = Field(default_factory=dict)


class BiometricCreate(BiometricBase):
    pass


class BiometricUpdate(BaseModel):
    type: Optional[BiometricType] = None
    data: Optional[bytes] = None
    compressed_data: Optional[bytes] = None
    thumbnail: Optional[bytes] = None
    embedding: Optional[List[float]] = None
    hash_checksum: Optional[str] = None
    encryption_method: Optional[str] = None
    is_active: Optional[bool] = None
    meta_info: Optional[Dict[str, Any]] = None


class BiometricResponse(BaseModel):
    id: str
    client_id: str
    type: BiometricType
    hash_checksum: Optional[str]
    encryption_method: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    meta_info: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True
