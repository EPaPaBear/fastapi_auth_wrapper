from fastapi import APIRouter, Depends
from fastapi_simplified.schemas.requests.create_user_request import CreateUserRequest
from fastapi_simplified.schemas.responses.user_response import *
from fastapi_simplified.schemas.responses.token_response import *
from fastapi_simplified.security.service.authentication import *
from fastapi_simplified.services.user_service import UserService
from fastapi_simplified.schemas.requests.create_user_request import BasicUserInfo
from fastapi_simplified.exceptions.resource_exceptions import IllegalArgumentException

auth_router = APIRouter()

# Pass the concrete implementation of UserDetailService
auth: UserService = make_user_detail_Service(UserService())

@auth_router.post("/signUp", response_model=User)
def signUp(new_user: CreateUserRequest):
    if not isinstance(new_user, BasicUserInfo):
        raise IllegalArgumentException()
    return auth.create_user(user_info=new_user)

@auth_router.post("/token", response_model=Token)
async def signIn(user_form: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(user_form)

@auth_router.get("/me", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user_info)):
    return current_user
