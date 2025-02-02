from src.core.product.dto.product import UpdateProductDTO
from src.core.product.entities.product import Product
from src.core.product.interfaces.repositories.product import IProductRepository


class ProductService:
    def __init__(self, repository: IProductRepository):
        self._repository = repository

    async def create_product(self, product: Product) -> None:
        await self._repository.add_product_on_db(product)

    async def update_product(self, product_id: int, update_product: UpdateProductDTO) -> None:
        await self._repository.update_product_on_db(product_id, update_product)

    async def delete_product(self, product_id: int) -> None:
        await self._repository.delete_product_from_db(product_id)
