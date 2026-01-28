from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_access_token
from app.models.medicine import MedicineResponse, MedicineCreate, MedicineUpdate
from app.services.medicine_service import (
    create_medicine,
    get_user_medicines,
    get_medicine_by_id,
    update_medicine,
    delete_medicine
)

# Initialize API router
router = APIRouter()

# HTTP Bearer security scheme for JWT
security = HTTPBearer()

# -------------------------------
# JWT Dependency
# -------------------------------
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verify the JWT token from the request and return the current user's payload.

    :param credentials: HTTP Bearer credentials containing the JWT token
    :return: Payload dictionary from JWT if valid
    :raises HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload


# -------------------------------
# CREATE Medicine Record
# -------------------------------
@router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
async def create_medicine_record(
    medicine: MedicineCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new medicine record for the current user.

    :param medicine: MedicineCreate model with medicine details
    :param current_user: Payload of the currently authenticated user
    :return: Created medicine record
    """
    try:
        medicine_record = create_medicine(
            medicine=medicine,
            user_id=current_user["user_id"]
        )
        return medicine_record

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create medicine record: {str(e)}"
        )


# -------------------------------
# GET All Medicines for User
# -------------------------------
@router.get("/", response_model=list[MedicineResponse])
async def list_user_medicines(
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve all medicine records for the current user.

    :param current_user: Payload of the currently authenticated user
    :return: List of medicine records
    """
    try:
        medicines = get_user_medicines(user_id=current_user["user_id"])
        return medicines

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch medicines: {str(e)}"
        )


# -------------------------------
# GET Single Medicine
# -------------------------------
@router.get("/{medicine_id}", response_model=MedicineResponse)
async def get_medicine(
    medicine_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a single medicine record by ID for the current user.

    :param medicine_id: ID of the medicine
    :param current_user: Payload of the currently authenticated user
    :return: Medicine record
    """
    try:
        medicine = get_medicine_by_id(
            medicine_id=medicine_id,
            user_id=current_user["user_id"]
        )
        return medicine

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch medicine: {str(e)}"
        )


# -------------------------------
# UPDATE Medicine Record
# -------------------------------
@router.put("/{medicine_id}", response_model=MedicineResponse)
async def update_medicine_record(
    medicine_id: int,
    medicine: MedicineUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing medicine record for the current user.

    :param medicine_id: ID of the medicine to update
    :param medicine: MedicineUpdate model with fields to update
    :param current_user: Payload of the currently authenticated user
    :return: Updated medicine record
    """
    try:
        updated = update_medicine(
            medicine_id=medicine_id,
            updated_data=medicine,
            user_id=current_user["user_id"]
        )
        return updated

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update medicine record: {str(e)}"
        )


# -------------------------------
# DELETE Medicine Record
# -------------------------------
@router.delete("/{medicine_id}", status_code=status.HTTP_200_OK)
async def delete_medicine_record(
    medicine_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a medicine record by ID for the current user.

    :param medicine_id: ID of the medicine to delete
    :param current_user: Payload of the currently authenticated user
    :return: Success message if deletion succeeds
    :raises HTTPException: If record not found or any internal error occurs
    """
    try:
        delete_medicine(
            medicine_id=medicine_id,
            user_id=current_user["user_id"]
        )
        return {
            "message": f"Medicine record with ID {medicine_id} has been successfully deleted."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete record: {str(e)}"
        )
