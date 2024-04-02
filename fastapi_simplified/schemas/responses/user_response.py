from pydantic import BaseModel

class SecurityDetails(BaseModel):
    disabled : bool = False

# Schema for response body for one user
class User(SecurityDetails):
    id: int
    username: str
    email: str
    name: str
    surname: str
    

    class Config:
        from_attributes = True


# Schema for response body for list of users
class PaginatedUsersInfo(BaseModel):
    limit: int = 10
    offset: int = 0
    data: list[User]