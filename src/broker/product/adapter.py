from src.broker.product.schemas import CreateProductBrokerSchema, DeleteProductBrokerSchema, \
    UpdateProductBrokerSchema
from src.core.product.dto.product import UpdateProductDTO
from src.core.product.entities.product import Product
from src.core.product.services.product import ProductService


class FromBrokerToProductServiceAdapter:
    def __init__(self, service: ProductService):
        self._service = service

    async def create_product(self, product_schema: CreateProductBrokerSchema) -> None:
        create_product_data = product_schema.model_dump(by_alias=True)
        product = Product(**create_product_data)
        await self._service.create_product(product)

    async def update_product(self, product_schema: UpdateProductBrokerSchema) -> None:
        update_product_data = product_schema.model_dump(exclude_unset=True, exclude_none=True, by_alias=True)
        update_product_dto = UpdateProductDTO(**update_product_data)
        await self._service.update_product(product_schema.product_id, update_product_dto)

    async def delete_product(self, product_schema: DeleteProductBrokerSchema):
        await self._service.delete_product(product_schema.product_id)
