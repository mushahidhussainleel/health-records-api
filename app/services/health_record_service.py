# app/services/health_record_service.py

from datetime import datetime
from fastapi import UploadFile
from typing import Optional

from app.utils.cleanup_file_storage import remove_health_record_file
from app.utils.file_helper import generate_file_hash, save_health_record_file
from app.models.health_record import HealthRecordCreate
from app.database.health_record_store import health_records_data, next_record_id


def create_health_record(
    user_id: int,
    record_data: HealthRecordCreate,
    file: UploadFile = None
) -> dict:
    """
    Create a new health record for a user.

    - Prevents duplicate record_type + title per user
    - Prevents duplicate file uploads using file hash
    - Supports optional file upload with version tracking
    """

    file_path = None
    file_hash = None

    # Handle file upload and duplicate file detection
    if file:
        file_hash = generate_file_hash(file)

        # Check for duplicate file content across user's records
        for record in health_records_data.values():
            if record["user_id"] == user_id:
                for version in record.get("file_versions", []):
                    if version.get("file_hash") == file_hash:
                        raise ValueError("This file has already been uploaded.")

        # Save file if no duplicate found
        file_path = save_health_record_file(file, user_id)

    global next_record_id
    now = datetime.utcnow()

    record = {
        "record_id": next_record_id,
        "user_id": user_id,
        "title": record_data.title,
        "description": record_data.description,
        "record_type": record_data.record_type,
        "test_result": record_data.test_result,
        "doctor_prescriptions": record_data.doctor_prescriptions,
        "record_date": record_data.record_date,
        "file_url": file_path,
        "file_versions": [],
        "created_at": now,
        "updated_at": now,
    }

    # Add initial file version if file exists
    if file_path:
        record["file_versions"].append({
            "file_url": file_path,
            "file_hash": file_hash,
            "uploaded_at": now
        })

    health_records_data[next_record_id] = record
    next_record_id += 1

    return record


def get_health_record_by_id(record_id: int, user_id: int) -> dict:
    """
    Fetch a single health record and validate user ownership.
    """
    record = health_records_data.get(record_id)

    if not record:
        raise ValueError("Health record not found. Please create one first.")

    if record["user_id"] != user_id:
        raise ValueError("Unauthorized access.")

    return record


def get_health_record_history(record_id: int, user_id: int) -> dict:
    """
    Fetch limited health record metadata (doctor-safe view).

    Exposes:
    - Record ID, title, type, date
    - Current file and version history

    Does NOT expose sensitive medical data.
    """
    record = get_health_record_by_id(record_id, user_id)

    return {
        "record_id": record["record_id"],
        "user_id": record["user_id"],
        "title": record["title"],
        "record_type": record.get("record_type", ""),
        "record_date": record.get("record_date", ""),
        "current_file": record.get("file_url", ""),
        "versions": record.get("file_versions", []),
        "created_at": record.get("created_at", ""),
        "updated_at": record.get("updated_at", "")
    }


def update_health_record(
    record_id: int,
    user_id: int,
    updated_data: HealthRecordCreate,
    file: Optional[UploadFile] = None
) -> dict:
    """
    Update an existing health record.

    - Prevents duplicate record_type + title per user
    - Prevents duplicate file content
    - Supports file versioning
    """

    # Fetch existing record
    record = get_health_record_by_id(record_id, user_id)

     # 🔒 Prevent changing immutable fields
    if (
        updated_data.title != record["title"]
        or updated_data.record_type != record["record_type"]
    ):
        raise ValueError(
            "Title and record type cannot be changed once created."
        )
    

    # Handle optional file upload
    if file:
        file_hash = generate_file_hash(file)

        # Check duplicate file across user's records
        for record in health_records_data.values():
            if record["user_id"] == user_id:
                for version in record.get("file_versions", []):
                    if version.get("file_hash") == file_hash:
                        raise ValueError("This file has already been uploaded.")

        # Save new file
        file_path = save_health_record_file(file, user_id)
        now = datetime.utcnow()

        # Append new version
        record["file_versions"].append({
            "file_url": file_path,
            "file_hash": file_hash,
            "uploaded_at": now
        })

        # Update latest file reference
        record["file_url"] = file_path

    # Update record fields
    record.update({
        "title": updated_data.title,
        "description": updated_data.description,
        "record_type": updated_data.record_type,
        "test_result": updated_data.test_result,
        "doctor_prescriptions": updated_data.doctor_prescriptions,
        "record_date": updated_data.record_date,
        "updated_at": datetime.utcnow(),
    })

    return record


def delete_health_record(record_id: int, user_id: int) -> None:
    """
    Delete a health record and all associated files.
    """
    record = get_health_record_by_id(record_id, user_id)

    # Remove all stored files
    for file_info in record.get("file_versions", []):
        remove_health_record_file(file_info["file_url"])

    # Remove record from storage
    del health_records_data[record_id]
