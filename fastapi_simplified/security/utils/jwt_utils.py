from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(r"resources/.env")

# Fetch environment variables
secret_key = os.getenv("JWT_SECRET_KEY")
algorithm = os.getenv("JWT_ALGORITHM")
expiry = float(os.getenv("JWT_EXPIRES_IN"))

def create_access_token(data : dict) -> str:
    """
    Create an access token with the provided data.

    Parameters
    ----------
    * data : `dict` \\
        The data to be encoded into the token.

    Returns
    -------
    * `str` \\
        The encoded JWT access token.
    """
    # Prepare data for encoding
    to_encode = data.copy()
    expire = timedelta(minutes=expiry) + datetime.now(timezone.utc)
    to_encode.update({"expires": expire.isoformat()})
    
    # Encode JWT token
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_claim(token:str, key:str) -> str:
    """
    Get the claim value from the provided JWT token.

    Parameters
    ----------
    * token : `str` \\
        The JWT token.
    * key : `str` \\
        The key of the claim to retrieve.

    Returns
    -------
    * `str` \\
        The value of the claim specified by the key.
    """
    # Decode JWT token and retrieve claim
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    claim : str = payload.get(key)
    
    # Return claim value
    if claim is not None:
        return claim