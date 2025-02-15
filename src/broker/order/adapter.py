from src.broker.order.schemas import PrepareOrderBrokerSchema
from src.core.basket.dto.product_on_basket import ProductOnBasketFilter
from src.core.basket.services.basket import BasketService


class FromOrderConsumerToBasketServiceAdapter:
    def __init__(self, service: BasketService):
        self._service = service

    async def pay_for_products_in_basket(
            self,
            order_schema: PrepareOrderBrokerSchema,
    ) -> None:
        order_data = order_schema.model_dump()
        await self._service.pay_for_products_in_basket(**order_data)
