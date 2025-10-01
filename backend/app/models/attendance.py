from pydantic import BaseModel
from datetime import datetime


class AttendanceBase(BaseModel):
    customer_id: str


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    id: str
    check_in_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True
