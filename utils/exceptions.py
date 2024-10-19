from fastapi import HTTPException, status

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication required", headers: dict = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)

class UserNotFoundError(HTTPException):
    def __init__(self, detail: str = "User not found", headers: dict = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)

class BookNotFoundError(HTTPException):
    def __init__(self, detail: str = "Book not found", headers: dict = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)

class BookNotAvailableError(HTTPException):
    def __init__(self, detail: str = "Book is not available", headers: dict = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)

class BookAlreadyBorrowedError(HTTPException):
    def __init__(self, detail: str = "Book is already borrowed", headers: dict = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)

class InvalidCredentialsError(HTTPException):
    def __init__(self, detail: str = "Invalid credentials", headers: dict = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)

class EmailAlreadyExistsError(HTTPException):
    def __init__(self, detail: str = "Email already exists", headers: dict = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)

class UsernameAlreadyExistsError(HTTPException):
    def __init__(self, detail: str = "Username already exists", headers: dict = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)

class InvalidTokenError(HTTPException):
    def __init__(self, detail: str = "Invalid token", headers: dict = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "Database error", headers: dict = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, headers=headers)

class APIError(HTTPException):
    def __init__(self, detail: str = "API error", headers: dict = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, headers=headers)

class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal server error", headers: dict = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, headers=headers)