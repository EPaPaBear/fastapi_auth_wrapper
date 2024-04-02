from fastapi_simplified.models.generics.auditable import * 

class User(Auditable):

    """
    A base user class that other specific user types can derive from.
    
    This class provides basic user information and includes fields that are common
    across different user types. It serves as the foundation for defining custom user
    implementations.

    Attributes
    -----------
    * id : `Integer`\\
        The row id

    * username : `String`\\
        The username of the user
        
    * password : `String`\\
        The password of the user
    
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))