# `fastapi_simplified`

A simplified FastAPI wrapper library for Spring-Boot-familiar developers and also for simple authentication.

## Table of Contents

- [`fastapi_simplified`](#fastapi_simplified)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Neccessary Setup](#neccessary-setup)
    - [Creating Entities](#creating-entities)
    - [Custom User Authentication](#custom-user-authentication)
      - [Implement `UserDetailsRepository`](#implement-userdetailsrepository)
      - [Implement `UserDetailService`](#implement-userdetailservice)
      - [Define Routes](#define-routes)
    - [Expose Routes via API](#expose-routes-via-api)

## Installation

To install `fastapi_simplified`, you can use pip:

```bash
pip install Path/To/fastapi_simplified.whl
```

## Usage

### Neccessary Setup
Before we start, we need to include some folders and files needed to run our application. We need to include a `/resources` folder in our project. This should have a `.env` file for keeping sensitive information needed - akin to _application.properties_ in spring boot. The primary contents of our `.env` file should look like so:

``` properties
# Database url - e.g. platform+driver://useername:passowrd@localhost:port/db_name
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/db_name"

# Security configs (optional if no auth needed)
JWT_SECRET_KEY = "32-bithexstring"
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN = 60 # in minutes
```

### Creating Entities
The fastapi_simplified library provides a convenient way to create entities by inheriting the Auditable class. Here's an example of creating a custom user entity:

```python
from fastapi_simplified.models.utils.security_details import SecurityDetails
from sqlalchemy.schema import Column
from sqlalchemy.types import *

class CustomUser(SecurityDetails):
    """
    Custom user entity inheriting from Auditable class.
    """

    __tablename__ = "users"

    # Additional fields
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    surname = Column(String(255))

```
Creating a custom user entity **must** inherit the `SecurityDetails` class. This is a mixin class for the default user class that has default security detail information such as account expiry, enabled status etc.

Creating non-user focused entities should inherit the `Auditable` class, like so;

```python
from fastapi_simplified.models.generics.auditable import Auditable
from sqlalchemy.schema import Column
from sqlalchemy.types import *


class CustomEntity(Auditable):

    __tablename__ = "custom_entity"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)

    # Additional information
```

### Custom User Authentication

To implement custom user authentication, you must implement the provided `UserDetailService` and `UserDetailsRepository` interfaces.

#### Implement `UserDetailsRepository`

```python
from fastapi_simplified.repositories.generics.i_user_repository import UserDetailsRepository
from fastapi_simplified.repositories.generics.generic_repository import GenericRepository
from custom_impl.models.user import CustomUser

class ConcreteUserDetailsRepository(UserDetailsRepository, GenericRepository):

    def __init__(self, model:CustomUser) -> None:
        super().__init__(model)

    def find_by_username(self, username: str) -> CustomUser:
        # Custom logic goes here ...
```

#### Implement `UserDetailService`

```python
from passlib.context import CryptContext
from fastapi_simplified.services.generics.user_details_service import UserDetailService
from custom_impl.repo import ConcreteUserDetailsRepository
from custom_impl.models.user import CustomUser

class ConcreteUserDetailService(UserDetailService):

    def __init__(self) -> None:
        self.repo = ConcreteUserDetailsRepository(CustomUser)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_by_username_password(self, username:str, password:str) -> CustomUser:
        # Custom logic goes here ...
        
    def get_by_username(self, username:str) -> TestUser:
        # Custom logic goes here ...
```

#### Define Routes
```python
from fastapi import APIRouter, Depends
from fastapi_simplified.security.service.authentication import *
from fastapi_simplified.schemas.responses.token_response import Token

auth_router = APIRouter()

@auth_router.post("/token", response_model=Token)
async def signIn(user_form: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token(user_form)
```

### Expose Routes via API
You can define additional API routes using FastAPI's APIRouter along with the auth_router for authentication routes. Here's an example:

```python

from fastapi import FastAPI
from custom_impl.controller.auth_routes import *

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["custom user"])

```

This will include the authentication routes under the /auth prefix.


That's it! You've now successfully set up custom user authentication and defined API routes using the fastapi_simplified library.