# app/utils/cleanup_file_storage.py

import os

def remove_health_record_file(file_path: str):
    """
    Remove a health record file from storage if it exists.

    :param file_path: Full path of the file to be deleted
    """
    try:
        # Check if the file exists before deleting
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted: {file_path}")
        else:
            # File path does not exist
            print(f"File not found: {file_path}")
    except Exception as e:
        # Handle any unexpected error during file deletion
        print(f"Failed to delete file {file_path}: {e}")
