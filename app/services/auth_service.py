from app.database.user_store import users_data, next_user_id
from app.core.password import hash_password, verify_password
from typing import Optional

# -------------------------------
# Create a new user
# -------------------------------
def create_user(
    name: str, 
    email: str, 
    age: int, 
    country: str,  
    password: str, 
    purpose: Optional[str] = None
):
    """
    Create a new user and store it in the users_data dictionary.
    
    :param name: User's full name
    :param email: User's email address (must be unique)
    :param age: User's age
    :param country: User's country
    :param password: User's plain text password
    :param purpose: Optional purpose or description of the user
    :return: Dictionary containing the created user data
    :raises ValueError: If a user with the same email already exists
    """
    global next_user_id

    # Check if user already exists
    if email in users_data:
        raise ValueError("User already exists")

    # Create user dictionary with hashed password
    user = {
        "user_id": next_user_id,
        "name": name,
        "age": age,
        "email": email,
        "country": country,
        "password_hash": hash_password(password),
        "purpose": purpose
    }

    # Store user and increment next user ID
    users_data[email] = user
    next_user_id += 1

    return user

# -------------------------------
# Authenticate existing user
# -------------------------------
def authenticate_user(email: str, password: str) -> dict | None:
    """
    Verify a user's email and password.

    :param email: User's email address
    :param password: User's plain text password
    :return: User dictionary if authentication succeeds, otherwise None
    """
    # Retrieve user from stored data
    user = users_data.get(email)
    if not user:
        return None

    # Check if the password matches
    if verify_password(password, user["password_hash"]):
        return user

    return None
