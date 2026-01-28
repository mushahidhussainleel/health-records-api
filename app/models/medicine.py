from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date, datetime

# -------------------------------
# Medicine Create Model
# -------------------------------
class MedicineCreate(BaseModel):
    """
    Model for creating a new medicine record.
    """
    medicine_name: str = Field(..., min_length=2, max_length=100)
    dosage: str = Field(..., description="e.g. 500mg, 1 tablet")
    frequency: Optional[str] = Field(
        None, description="e.g. Once a day, Twice a day"
    )
    start_date: date
    end_date: Optional[date] = None
    prescription_reason: Optional[str] = Field(
        None, description="Reason why the doctor prescribed this medicine"
    )
    side_effect: Optional[str] = Field(
        None, description="Positive or negative effects observed by the patient"
    )
    prescribed_by: Optional[str] = Field(
        None, description="Doctor's name (optional)"
    )

# -------------------------------
# Medicine Update Model
# -------------------------------
class MedicineUpdate(BaseModel):
    """
    Model for updating existing medicine details.
    """
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    side_effect: Optional[str] = None
    prescription_reason: Optional[str] = None
    prescribed_by: Optional[str] = None

# -------------------------------
# Medicine Response Model
# -------------------------------
class MedicineResponse(BaseModel):
    """
    Model to structure the response when returning medicine data.
    """
    medicine_id: int
    user_id: int

    medicine_name: str
    dosage: str
    frequency: Optional[str]

    start_date: date
    end_date: Optional[date]

    prescription_reason: Optional[str]
    side_effect: Optional[str]
    prescribed_by: Optional[str]

    # List to store history of medicine updates
    medicine_history: List[Dict] = []

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
