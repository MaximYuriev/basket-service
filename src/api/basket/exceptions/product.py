from fastapi import HTTPException, status


class HTTPProductException(HTTPException):
    pass


class HTTPProductNotFoundException(HTTPProductException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg,
        )


class HTTPProductAlreadyInBasketException(HTTPProductException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )