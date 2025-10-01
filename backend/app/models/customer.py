from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import date, datetime
from enum import Enum
import re


class DocumentType(str, Enum):
    CC = "CC"  # Cédula de Ciudadanía
    TI = "TI"  # Tarjeta de Identidad
    CE = "CE"  # Cédula de Extranjería
    PP = "PP"  # Pasaporte


class GenderType(str, Enum):
    M = "M"  # Masculino
    F = "F"  # Femenino
    O = "O"  # Otro


class RecordStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"


class CustomerBase(BaseModel):
    dni_type: DocumentType
    dni_number: str = Field(..., min_length=5, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    second_last_name: Optional[str] = Field(None, max_length=100)
    phone: str = Field(..., min_length=7, max_length=20)
    alternative_phone: Optional[str] = Field(None, min_length=7, max_length=20)
    birth_date: date
    gender: GenderType
    address: Optional[str] = None
    status: RecordStatus = RecordStatus.ACTIVE
    is_active: bool = True
    meta_info: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @field_validator('dni_number')
    @classmethod
    def validate_dni_number(cls, v: str) -> str:
        if not re.match(r'^[0-9A-Za-z-]+$', v):
            raise ValueError('DNI number must contain only alphanumeric characters and hyphens')
        return v

    @field_validator('phone', 'alternative_phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r'^[\d\s\-\+\(\)]+$', v):
            raise ValueError('Phone must contain only numbers, spaces, and phone symbols')
        return v


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    dni_type: Optional[DocumentType] = None
    dni_number: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    phone: Optional[str] = None
    alternative_phone: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[GenderType] = None
    address: Optional[str] = None
    status: Optional[RecordStatus] = None
    is_active: Optional[bool] = None
    meta_info: Optional[Dict[str, Any]] = None


class CustomerResponse(CustomerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
