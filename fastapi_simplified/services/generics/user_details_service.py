import abc

class UserDetailService(metaclass=abc.ABCMeta):
    """
    Abstract base class for user detail services.

    This class defines the interface that user detail service implementations should adhere to.

    Methods
    -------
    * __subclasshook__(subclass)
        Check if a class is a subclass of `UserDetailService`.
    * get_by_username_password(username: `str`, password: `str`) -> `SecurityDetails`
        Get a user by username and verify password.
    * get_by_username(username: `str`) -> `SecurityDetails`
        Get a user by username.

    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_by_username') and 
                callable(subclass.load_data_source) or
                NotImplemented)

    @abc.abstractmethod
    def get_by_username_password(self, username:str, password:str):
        """
        Get a user by username and verify password.

        Parameters
        ----------
        * username : `str`
            The username of the user.
        * password : `str`
            The password to verify.

        Returns
        -------
        * `SecurityDetails`
            The user details if the username and password are valid.

        Raises
        ------
        * `NotImplementedError`
            If the method is not implemented by the subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_username(self, username:str):
        """
        Get a user by username.

        Parameters
        ----------
        * username : `str`
            The username of the user to retrieve.

        Returns
        -------
        * `SecurityDetails`
            The user details corresponding to the provided username.

        Raises
        ------
        * `NotImplementedError`
            If the method is not implemented by the subclass.

        """
        raise NotImplementedError