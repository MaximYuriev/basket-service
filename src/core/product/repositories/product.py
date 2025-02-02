from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.product.dto.product import UpdateProductDTO
from src.core.product.entities.product import Product
from src.core.product.exceptions.product import ProductNotFoundException
from src.core.product.interfaces.repositories.product import IProductRepository
from src.core.product.models.product import ProductModel


class ProductRepository(IProductRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_product_on_db(self, product: Product) -> None:
        product_model = ProductModel.create_from_entity(product)
        self._session.add(product_model)
        await self._session.commit()

    async def update_product_on_db(self, product_id: int, update_product: UpdateProductDTO) -> None:
        product_model = await self._get_product_from_db(product_id)
        update_product_data = update_product.__dict__
        for key, value in update_product_data.items():
            if value is not None:
                setattr(product_model, key, value)
        await self._session.commit()

    async def delete_product_from_db(self, product_id: int) -> None:
        product_model = await self._get_product_from_db(product_id)
        await self._session.delete(product_model)
        await self._session.commit()

    async def _get_product_from_db(self, product_id: int) -> ProductModel:
        query = select(ProductModel).where(ProductModel.product_id == product_id)
        product_model = await self._session.scalar(query)
        if product_model is None:
            raise ProductNotFoundException(product_id)
        return product_model
