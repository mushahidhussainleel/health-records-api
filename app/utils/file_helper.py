# app/utils/file_helper.py

import os
import shutil
import uuid
import hashlib
from fastapi import UploadFile


def generate_file_hash(file: UploadFile) -> str:
    """
    Generate a SHA256 hash for an uploaded file.

    This hash can be used to detect duplicate files
    or verify file integrity.
    """
    # Move file pointer to the beginning
    file.file.seek(0)

    # Initialize SHA256 hash object
    sha256 = hashlib.sha256()

    # Read the file in chunks to handle large files
    while chunk := file.file.read(8192):  # Walrus operator for reading chunks
        sha256.update(chunk)

    # Reset file pointer after reading
    file.file.seek(0)

    return sha256.hexdigest()


def save_health_record_file(file: UploadFile, user_id: int) -> str:
    """
    Save an uploaded health record file in a user-specific folder.

    The file is stored with a unique name to avoid conflicts.

    :param file: Uploaded file object
    :param user_id: ID of the user uploading the file
    :return: Full file path where the file is saved
    """
    # Base directory for storing health record files
    base_dir = "storage/health_records"

    # Create user-specific directory
    user_dir = os.path.join(base_dir, f"user_{user_id}")
    os.makedirs(user_dir, exist_ok=True)

    # Generate a unique file name while keeping the original extension
    file_ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(user_dir, unique_name)

    # Save the file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path
