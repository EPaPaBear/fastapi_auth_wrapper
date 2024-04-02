from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_simplified.schemas.responses.token_response import *
from fastapi_simplified.services.generics.user_details_service import UserDetailService
from fastapi_simplified.security.utils.jwt_utils import *
from fastapi_simplified.exceptions.authentication_exceptions import *
from fastapi_simplified.models.utils.security_details import SecurityDetails
from fastapi_simplified.services.user_service import UserService


user_service: UserDetailService = None 

def make_user_detail_Service(service: UserDetailService):
    """
    Set the user detail service for authentication.

    Parameters
    ----------
    * service : `UserDetailService` \\
        The user detail service providing user-related operations.

    Returns
    -------
    * `UserDetailService` \\
        The set user detail service.
    """
    global user_service
    user_service = service
    return user_service


async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Generate an access token for the provided user credentials.

    Parameters
    ----------
    * form : `OAuth2PasswordRequestForm`, `optional` \\
        The user credentials submitted through the login form.

    Returns
    -------
    * `Token` \\
        The generated access token.
    
    Raises
    ------
    * `BadCredentialsException` \\
        If the provided credentials are invalid.
    * `InactiveUserException` \\
        If the user account is inactive.
    """
    user: SecurityDetails = user_service.get_by_username_password(username=form.username, password=form.password)
    if not user:
        raise BadCredentialsException()
    if user.disabled:
        raise InactiveUserException()
    # Add other specific user security details checks here

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user_information(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    """
    Retrieve current user information from the provided JWT token.

    Parameters
    ----------
    * token : `str`, `optional` \\
        The JWT token obtained from the request.

    Returns
    -------
    * `SecurityDetails` \\
        The user information retrieved from the token.

    Raises
    ------
    * `BadCredentialsException` \\
        If the token is invalid.
    """
    try:
        username = get_claim(token=token, key="sub")
        token_data = TokenData(username=username)
    except JWTError:
        raise BadCredentialsException()

    user = user_service.get_by_username(token_data.username)
    if user is None:
        raise BadCredentialsException()

    return user


async def get_current_active_user_info(curr_user: SecurityDetails = Depends(get_current_user_information)):
    """
    Retrieve current active user information.

    Parameters
    ----------
    * curr_user : `SecurityDetails`, `optional` \\
        The current user information retrieved from the token.

    Returns
    -------
    * `SecurityDetails` \\
        The current active user information.

    Raises
    ------
    * `InactiveUserException` \\
        If the user account is inactive.
    """
    if curr_user.disabled:
        raise InactiveUserException()
    return curr_user