from fastapi import HTTPException, status


class HTTPBasketException(HTTPException):
    pass


class HTTPBasketAlreadyExistException(HTTPBasketException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
        )


class HTTPBasketNotFoundException(HTTPBasketException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg,
        )
