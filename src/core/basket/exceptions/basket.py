from src.core.base.exception import ApplicationException


class BasketException(ApplicationException):
    pass


class BasketNotFoundException(BasketException):
    @property
    def message(self) -> str:
        return "Корзина не найдена!"


class BasketAlreadyExistException(BasketException):
    @property
    def message(self) -> str:
        return "Корзина уже существует!"
