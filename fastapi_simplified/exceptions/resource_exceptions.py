from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")


class UsernameOrEmailAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists. Please try another one.")


class IllegalArgumentException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something unexpected happened that isn't your fault. Report this to your admin.")