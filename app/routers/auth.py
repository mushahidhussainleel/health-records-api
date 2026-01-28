from fastapi import APIRouter, HTTPException
from app.services.auth_service import create_user, authenticate_user
from app.models.user import SignupModel, LoginModel, UserResponseModel
from app.core.security import create_access_token

# Initialize API router
router = APIRouter()

@router.post("/signup", response_model=UserResponseModel)
async def signup(user: SignupModel):
    """
    Register a new user using the signup data.

    :param user: SignupModel containing user registration info
    :return: UserResponseModel with user ID, name, email, and success message
    :raises HTTPException: If a user with the same email already exists
    """
    try:
        # Create the new user using the auth service
        new_user = create_user(
            name=user.name,
            age=user.age,
            email=user.email,
            password=user.password,
            country=user.country,
            purpose=user.purpose
        )

        # Return structured response
        return {
            "user_id": new_user["user_id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "message": "User registered successfully!"
        }

    except ValueError as e:
        # Raise HTTP 400 error if user already exists
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: LoginModel):
    """
    Authenticate a user and return a JWT access token if credentials are correct.

    :param user: LoginModel containing email and password
    :return: Dictionary with access token, token type, and success message
    :raises HTTPException: If email or password is invalid
    """
    # Authenticate user using auth service
    authenticated_user = authenticate_user(user.email, user.password)

    if not authenticated_user:
        # Raise HTTP 401 error for invalid credentials
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Prepare data for JWT token
    token_data = {
        "user_id": authenticated_user["user_id"],
        "email": authenticated_user["email"]
    }

    # Create access token
    access_token = create_access_token(token_data)

    # Return token and success message
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful!"
    }
