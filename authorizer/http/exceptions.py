from fastapi import HTTPException, status


class HTTPAuthException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )


class HTTPTokenInvalidException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействительный!",
        )


class HTTPUnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходимо авторизоваться!",
        )


class HTTPUserIsNotAdminException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не обладает необходимыми правами!",
        )
