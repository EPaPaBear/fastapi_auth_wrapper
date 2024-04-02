from fastapi_simplified.models.generics.generic_user import *


class SecurityDetails(User):
    """
    A base class for defining common security information.

    This class serves as a mixin for defining common security-related attributes that
    can be shared across different user types. It inherits the `User` model to leverage its
    Pydantic definition for compatibility with `SQLAlchemy`.

    Attributes
    ----------
    * disabled : `boolean`\\
    The Disability status of the user
    """

    __abstract__ = True

    disabled = Column(Boolean)
