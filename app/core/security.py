import jwt
from dotenv import load_dotenv, find_dotenv
import os
from datetime import timedelta, datetime, timezone

# Load environment variables
load_dotenv(find_dotenv())

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Validate SECRET_KEY
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is missing! Check your .env file")

def create_access_token(data: dict, expire_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Creates a JWT access token with expiry time
    
    :param data: Data to include in the token (e.g., {"user_id": 5, "email": "user@example.com"})
    :param expire_delta: Token validity in minutes (default 30 minutes)
    :return: JWT token string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str) -> dict | None:
    """
    Verifies JWT token and returns payload
    
    :param token: JWT token string
    :return: Payload dict if valid, otherwise None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
