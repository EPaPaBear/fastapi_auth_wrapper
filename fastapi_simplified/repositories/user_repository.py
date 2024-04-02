from fastapi_simplified.repositories.generics.generic_repository import GenericRepository
from fastapi_simplified.repositories.generics.i_user_repository import UserDetailsRepository
from fastapi_simplified.models.custom_user import CustomUser


class UserRepository(UserDetailsRepository, GenericRepository):
    """
    User Repository class that implements `UserDetailsRepository` formal interface and inherits from `GenericRepository`.
    Includes methods for crud and additional methods.

    Attributes
    ----------
    Same as super

    Methods
    --------
    Same as super with additional methods
    * find_by_username(username:`str`) -> `CustomUser`
    """
    def __init__(self, model: CustomUser) -> None:
        super().__init__(model)

    def find_by_username(self, username:str) -> CustomUser:
        """
        Finds a user entity via username

        Parameters
        ------------
        * username : `str`\\
            The username of the user

        Returns
        --------
        * `User` **(Change return to the active user type)** : The found user
        """
        return self.db.query(self.model).filter(CustomUser.username == username).first()

