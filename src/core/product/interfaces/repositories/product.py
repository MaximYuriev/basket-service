from abc import ABC, abstractmethod

from src.core.product.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def add_product_on_db(self, product: Product) -> None:
        ...

    @abstractmethod
    async def update_product_on_db(self, product: Product) -> None:
        ...
