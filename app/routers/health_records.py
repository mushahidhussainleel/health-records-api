# app/routers/health_records_router.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form
)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import date

from app.core.security import verify_access_token
from app.models.health_record import HealthRecordCreate, HealthRecordResponse 
from app.services.health_record_service import (
    create_health_record,
    get_health_record_history,
    get_health_record_by_id,
    update_health_record,
    delete_health_record,
)

router = APIRouter()

security = HTTPBearer()


# Dependency to extract and verify JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload


@router.post(
    "/",
    response_model=HealthRecordResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_record(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    record_type: str = Form(...),
    test_result: Optional[str] = Form(None),
    doctor_prescriptions: Optional[str] = Form(None),
    record_date: date = Form(default=date.today()),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new health record with an initial file upload.
    Duplicate files are prevented using a SHA256 hash check.
    """
    try:
        
        # Build HealthRecordCreate object from form data
        record_data = HealthRecordCreate(
            title=title,
            description=description,
            record_type=record_type,
            test_result=test_result,
            doctor_prescriptions=doctor_prescriptions,
            record_date=record_date
        )

        # Create the health record using the service layer
        record = create_health_record(
            user_id=current_user["user_id"],
            record_data=record_data,
            file=file
        )

        return record

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create health record: {str(e)}"
        )


@router.get(
    "/{record_id}/history",
)
async def get_full_record_history(
    record_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve file history and basic metadata of a health record.
    Intended for doctor or limited-access views.
    """
    try:
        history = get_health_record_history(
            record_id=record_id,
            user_id=current_user["user_id"]
        )
        return history

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/{record_id}",
    response_model=HealthRecordResponse
)
async def get_record(
    record_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a single health record by its ID.
    Ownership is validated before returning data.
    """
    try:
        record = get_health_record_by_id(record_id=record_id, user_id=current_user["user_id"])
        return record
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch record: {str(e)}"
        )


@router.put(
    "/{record_id}",
    response_model=HealthRecordResponse,
    status_code=status.HTTP_200_OK
)
async def update_record(
    record_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    record_type: str = Form(...),
    test_result: Optional[str] = Form(None),
    doctor_prescriptions: Optional[str] = Form(None),
    record_date: date = Form(default=date.today()),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing health record.
    Prevents duplicate record type and title per user.
    Supports optional file versioning.
    """
    try:

        # Build updated HealthRecordCreate object
        updated_data = HealthRecordCreate(
            title=title,
            description=description,
            record_type=record_type,
            test_result=test_result,
            doctor_prescriptions=doctor_prescriptions,
            record_date=record_date
        )

        # Update the record using the service layer
        record = update_health_record(
            record_id=record_id,
            user_id=current_user["user_id"],
            updated_data=updated_data,
            file=file
        )

        return record

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update health record: {str(e)}"
        )


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_200_OK
)
async def delete_record(
    record_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a health record along with all associated files.
    """
    try:
        delete_health_record(
            record_id=record_id,
            user_id=current_user["user_id"]
        )
        return {
            "message": f"Health record with ID {record_id} has been successfully deleted."
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete record: {str(e)}"
        )
