from app.database.medicine_store import medicines_data, next_medicine_id
from app.models.medicine import MedicineCreate, MedicineResponse, MedicineUpdate
from datetime import datetime
from typing import Optional, List

# -------------------------------
# Create Medicine Record
# -------------------------------
def create_medicine(user_id: int, medicine: MedicineCreate) -> dict:
    """
    Create a new medicine record for a user.

    :param user_id: ID of the user
    :param medicine: MedicineCreate model with medicine details
    :return: Dictionary containing the created medicine record
    """
    global next_medicine_id
    now = datetime.utcnow()

    # Create medicine record dictionary
    medicine_record = {
        "medicine_id": next_medicine_id,
        "user_id": user_id,
        "medicine_name": medicine.medicine_name,
        "dosage": medicine.dosage,
        "frequency": medicine.frequency,
        "start_date": medicine.start_date,
        "end_date": medicine.end_date,
        "prescription_reason": medicine.prescription_reason,
        "side_effect": medicine.side_effect,
        "prescribed_by": medicine.prescribed_by,
        "medicine_history": [],  # History of updates
        "created_at": now,
        "updated_at": now,
    }

    # Take snapshot of initial state
    snapshot = {
        "updated_at": now,
        "data": {
            "medicine_name": medicine_record["medicine_name"],
            "dosage": medicine_record["dosage"],
            "frequency": medicine_record["frequency"],
            "start_date": medicine_record["start_date"],
            "end_date": medicine_record["end_date"],
            "prescription_reason": medicine_record["prescription_reason"],
            "side_effect": medicine_record["side_effect"],
            "prescribed_by": medicine_record["prescribed_by"],
            "created_at": medicine_record["created_at"],
            "updated_at": medicine_record["updated_at"],
        }
    }

    # Add snapshot to medicine history
    medicine_record["medicine_history"].append(snapshot)

    # Store medicine record and increment ID
    medicines_data[next_medicine_id] = medicine_record
    next_medicine_id += 1

    return medicine_record

# -------------------------------
# Get Medicine Record by ID
# -------------------------------
def get_medicine_by_id(medicine_id: str, user_id: int) -> MedicineResponse:
    """
    Retrieve a medicine record by its ID for a specific user.

    :param medicine_id: ID of the medicine
    :param user_id: ID of the user
    :return: MedicineResponse dictionary
    :raises ValueError: If record not found or unauthorized access
    """
    record = medicines_data.get(medicine_id)
    if not record:
        raise ValueError(f"Medicine record with ID {medicine_id} not found.")

    if record["user_id"] != user_id:
        raise ValueError("Unauthorized access.")

    return record

# -------------------------------
# Get All Medicines for a User
# -------------------------------
def get_user_medicines(user_id: int) -> List[MedicineResponse]:
    """
    Retrieve all medicine records for a specific user.

    :param user_id: ID of the user
    :return: List of medicine records
    """
    return [record for record in medicines_data.values() if record["user_id"] == user_id]

# -------------------------------
# Update Medicine Record
# -------------------------------
def update_medicine(medicine_id: int, user_id: int, updated_data: MedicineUpdate) -> MedicineResponse:
    """
    Update an existing medicine record partially.

    :param medicine_id: ID of the medicine
    :param user_id: ID of the user
    :param updated_data: MedicineUpdate model with fields to update
    :return: Updated medicine record
    """
    record = get_medicine_by_id(medicine_id, user_id)

    # Update only fields provided in updated_data
    if updated_data.dosage is not None:
        record["dosage"] = updated_data.dosage
    if updated_data.frequency is not None:
        record["frequency"] = updated_data.frequency
    if updated_data.side_effect is not None:
        record["side_effect"] = updated_data.side_effect
    if updated_data.prescription_reason is not None:
        record["prescription_reason"] = updated_data.prescription_reason
    if updated_data.prescribed_by is not None:
        record["prescribed_by"] = updated_data.prescribed_by

    record["updated_at"] = datetime.utcnow()

    # Append snapshot of current state to medicine_history
    snapshot = {
        "updated_at": datetime.utcnow(),
        "data": {
            "medicine_name": record["medicine_name"],
            "dosage": record["dosage"],
            "frequency": record["frequency"],
            "start_date": record["start_date"],
            "end_date": record["end_date"],
            "prescription_reason": record["prescription_reason"],
            "side_effect": record["side_effect"],
            "prescribed_by": record["prescribed_by"],
            "created_at": record["created_at"],
            "updated_at": record["updated_at"],
        }
    }

    record["medicine_history"].append(snapshot)
    return record

# -------------------------------
# Delete Medicine Record
# -------------------------------
def delete_medicine(medicine_id: int, user_id: int) -> None:
    """
    Delete a medicine record by its ID for a specific user.

    :param medicine_id: ID of the medicine
    :param user_id: ID of the user
    :raises ValueError: If record not found or unauthorized access
    """
    # Ensure record exists and user is authorized
    get_medicine_by_id(medicine_id, user_id)

    # Delete the record
    del medicines_data[medicine_id]
