from src.core.base.exception import ApplicationException


class ProductOnBasketException(ApplicationException):
    pass


class ProductOnBasketNotFoundException(ProductOnBasketException):
    @property
    def message(self) -> str:
        return 'Товар не найден!'


class ProductAlreadyInBasketException(ProductOnBasketException):
    @property
    def message(self) -> str:
        return 'Товар уже добавлен в корзину'