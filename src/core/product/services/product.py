from src.core.product.entities.product import Product
from src.core.product.interfaces.repositories.product import IProductRepository


class ProductService:
    def __init__(self, repository: IProductRepository):
        self._repository = repository

    async def create_product(self, product: Product) -> None:
        await self._repository.add_product_on_db(product)

    async def update_product(self):
        ...
