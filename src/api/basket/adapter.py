import uuid

from src.api.basket.filters import ProductOnBasketFilterSchema
from src.api.basket.schemas.basket import CreateBasketSchema, BasketSchema
from src.api.basket.schemas.product import AddProductSchema, UpdateProductSchema
from src.core.basket.dto.product_on_basket import UpdateProductOnBasketDTO, AddProductOnBasketDTO, ProductOnBasketFilter
from src.core.basket.services.basket import BasketService


class BasketServiceAdapter:
    def __init__(self, service: BasketService):
        self._service = service

    async def create_basket(
            self,
            create_basket_schema: CreateBasketSchema,
    ) -> None:
        await self._service.create_basket(create_basket_schema.basket_id)

    async def get_basket(
            self,
            basket_id: uuid.UUID,
            filters: ProductOnBasketFilterSchema,
    ) -> BasketSchema:
        product_on_basket_filter = None
        if filters.with_products_marked_for_order is not None:
            product_on_basket_filter = ProductOnBasketFilter(**filters.model_dump(by_alias=True))
        basket = await self._service.get_basket(basket_id, product_on_basket_filter)
        return BasketSchema.model_validate(basket, from_attributes=True)

    async def add_product_on_basket(
            self,
            basket_id: uuid.UUID,
            create_product_schema: AddProductSchema,
    ) -> None:
        added_product = AddProductOnBasketDTO(**create_product_schema.model_dump())
        await self._service.add_product_on_basket(added_product, basket_id)

    async def remove_product_from_basket(
            self,
            basket_id: uuid.UUID,
            product_id: int,
    ) -> None:
        await self._service.remove_product_from_basket(product_id, basket_id)

    async def update_product_on_basket(
            self,
            basket_id: uuid.UUID,
            product_id: int,
            update_product_schema: UpdateProductSchema,
    ) -> None:
        update_product_dto = UpdateProductOnBasketDTO(
            product_id=product_id,
            **update_product_schema.model_dump()
        )
        await self._service.update_product_on_basket(update_product_dto, basket_id)
