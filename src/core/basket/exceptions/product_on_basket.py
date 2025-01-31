from src.core.base.exception import ApplicationException


class ProductException(ApplicationException):
    pass


class ProductNotFoundException(ProductException):
    @property
    def message(self) -> str:
        return 'Товар не найден!'


class ProductAlreadyInBasketException(ProductException):
    @property
    def message(self) -> str:
        return 'Товар уже добавлен в корзину'