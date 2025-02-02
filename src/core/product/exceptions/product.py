from dataclasses import dataclass

from src.core.base.exception import ApplicationException


class ProductException(ApplicationException):
    pass


@dataclass
class ProductNotFoundException(ProductException):
    product_id: int

    @property
    def message(self) -> str:
        return f"Товар с {self.product_id=} не найден!"
