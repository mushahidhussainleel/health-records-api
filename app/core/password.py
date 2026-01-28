from passlib.context import CryptContext

# Initialize CryptContext with bcrypt scheme
# 'deprecated="auto"' will show a warning if any scheme is outdated
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",  
)

def hash_password(password: str) -> str:
    """
    Convert a plain password into a secure bcrypt hash.
    
    :param password: User's plain text password
    :return: Hashed password using bcrypt
    """
    # Hash the password and return it
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches the hashed password.
    
    :param plain_password: Password provided by the user
    :param hashed_password: Password stored in the database (hashed)
    :return: True if passwords match, otherwise False
    """
    # Compare the plain password with the hashed one and return the result
    return pwd_context.verify(plain_password, hashed_password)
