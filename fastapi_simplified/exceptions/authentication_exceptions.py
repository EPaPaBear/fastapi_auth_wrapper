from fastapi import HTTPException, status

class BadCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad Credentials")


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
