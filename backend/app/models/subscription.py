from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class SubscriptionBase(BaseModel):
    customer_id: str
    plan_id: str
    start_date: date
    end_date: date
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE


class SubscriptionCreate(BaseModel):
    customer_id: str
    plan_id: str
    start_date: date


class SubscriptionUpdate(BaseModel):
    status: Optional[SubscriptionStatus] = None
    end_date: Optional[date] = None


class SubscriptionResponse(SubscriptionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
