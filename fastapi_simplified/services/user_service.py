from fastapi_simplified.repositories.user_repository import UserRepository
from fastapi_simplified.models.custom_user import CustomUser
from fastapi_simplified.schemas.requests.create_user_request import CreateUserRequest
from passlib.context import CryptContext
from fastapi_simplified.exceptions.authentication_exceptions import *
from fastapi_simplified.exceptions.resource_exceptions import *
from fastapi_simplified.services.generics.user_details_service import UserDetailService


class UserService(UserDetailService):

    def __init__(self) -> None:
        self.repo = UserRepository(CustomUser)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def get_by_username_password(self, username:str, password:str) -> CustomUser:
        user = self.repo.find_by_username(username)
        if user:
            if self.pwd_context.verify(password, user.password):
                return user
            raise BadCredentialsException()
        raise ResourceNotFoundException()
        
    def get_by_username(self, username:str) -> CustomUser:
        return self.repo.find_by_username(username)

    def create_user(self, user_info:CreateUserRequest) -> CustomUser:
        new_user = CustomUser(**user_info.model_dump())
        new_user.password = self.pwd_context.hash(new_user.password)
        return self.repo.save(new_user)
        