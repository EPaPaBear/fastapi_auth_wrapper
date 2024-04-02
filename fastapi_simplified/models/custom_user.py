from fastapi_simplified.models.utils.security_details import *
from fastapi_simplified.models.utils.security_details import SecurityDetails


class CustomUser(SecurityDetails):

    __abstract__ = True
    #__tablename__ = "users"

    # Additional fields on top of the existing user class
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    surname = Column(String(255))

