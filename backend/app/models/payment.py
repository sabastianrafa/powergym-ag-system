from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class PaymentMethod(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    TRANSFER = "transfer"


class PaymentStatus(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    CANCELLED = "cancelled"


class PaymentBase(BaseModel):
    subscription_id: str
    customer_id: str
    amount: Decimal = Field(..., ge=0, decimal_places=2)
    payment_method: PaymentMethod
    status: PaymentStatus = PaymentStatus.COMPLETED
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: str
    payment_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
