from pydantic import BaseModel

# Basic User Information
class BasicUserInfo(BaseModel):
    """
    A wrapper `BaseModel` class that contains the  basic user information for authentication.

    Attrubutes
    -----------
    * username : `str`\\
        The username of the user
    * password: `str` \\
        The password of the user
    """
    username: str
    password: str


class SecurityDetails(BasicUserInfo):
    """
    A class that extends `BasicUserInfo` to include security details.

    This class adds additional security-related information to the basic user information
    defined in `BasicUserInfo`.

    Attributes
    ----------
    * disabled : `bool` \\
        The status indicating whether the user is disabled or not. Defaults to False.
    """
    disabled : bool = False


class CreateUserRequest(SecurityDetails):
    email: str
    name: str
    surname: str
