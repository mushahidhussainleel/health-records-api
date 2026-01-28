# app/models/health_record.py

from pydantic import BaseModel, Field
from typing import Optional , List
from datetime import datetime, date


# Health Record Create

class HealthRecordCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    record_type: str = Field(..., description="Lab Report, X-Ray, MRI, etc.")
    test_result: Optional[str] = Field(None, description="Positive/Negative/values")
    doctor_prescriptions: Optional[str] = None
    record_date: date = Field(default_factory=date.today)



# Health Record Response

class HealthRecordResponse(BaseModel):
    record_id: int
    user_id: int
    title: str
    description: Optional[str]
    record_type: str
    test_result: Optional[str]
    doctor_prescriptions: Optional[str]
    file_url: Optional[str]   
    record_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True