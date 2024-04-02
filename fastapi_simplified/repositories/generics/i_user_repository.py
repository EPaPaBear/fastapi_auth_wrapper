import abc

class UserDetailsRepository(metaclass=abc.ABCMeta):
    """
    Abstract base class for user-entity-related repositories.

    In terms of security implementation, classes representing repositories for user entities
    must extend this class and define the `find_by_username` method.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        """
        Check if a class is a subclass of UserDetailsRepository.

        Parameters
        ----------
        * subclass : `type` \\
            The class to check for subclassing UserDetailsRepository.

        Returns
        -------
        * `bool` or `NotImplemented` \\
            True if subclass has a callable `find_by_username` method, False otherwise.
            NotImplemented if subclass is not checked for subclassing.
        """
        return (hasattr(subclass, 'find_by_username') and 
                callable(subclass.find_by_username) or
                NotImplemented)

    @abc.abstractmethod
    def find_by_username(self, username:str):
        """
        Abstract method to find a user by username.

        This method should be implemented by subclasses to retrieve a user entity
        from the data source based on the provided username.

        Parameters
        ----------
        * username : `str` \\
            The username of the user to find.

        Returns
        -------
        * `User` or `None` \\
            The user entity corresponding to the provided username, or None if not found.

        Raises
        ------
        * `NotImplementedError` \\
            If the method is not implemented by the subclass.
        """
        raise NotImplementedError