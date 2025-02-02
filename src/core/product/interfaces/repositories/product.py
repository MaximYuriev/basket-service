from abc import ABC, abstractmethod

from src.core.product.dto.product import UpdateProductDTO
from src.core.product.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def add_product_on_db(self, product: Product) -> None:
        ...

    @abstractmethod
    async def update_product_on_db(self, product_id: int, update_product: UpdateProductDTO) -> None:
        ...

    @abstractmethod
    async def delete_product_from_db(self, product_id: int) -> None:
        ...
