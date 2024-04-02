from pydantic import BaseModel

class Token(BaseModel):
    """
    Model representing an authentication token.

    Attributes
    ----------
    * access_token : `str` \\
        The access token string.
    * token_type : `str` \\
        The type of token (e.g., "bearer").

    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None