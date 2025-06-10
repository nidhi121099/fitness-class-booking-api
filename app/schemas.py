from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class FitnessClassBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructor: str
    start_time: datetime
    duration_minutes: int = Field(60, gt=0)
    total_slots: int = Field(10, gt=0)
    available_slots: int = Field(10, ge=0)

class FitnessClassCreate(FitnessClassBase):
    pass

class FitnessClassResponse(FitnessClassBase):
    id: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BookingRequest(BaseModel):
    class_id: str
    client_name: str
    client_email: EmailStr

class BookingResponse(BaseModel):
    id: str
    class_id: str
    class_name: str
    client_name: str
    client_email: EmailStr
    booking_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }