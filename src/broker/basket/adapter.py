from src.broker.basket.schemas import CreateBasketBrokerSchema
from src.core.basket.services.basket import BasketService


class FromBrokerToBasketServiceAdapter:
    def __init__(self, service: BasketService):
        self._service = service

    async def create_basket(self, create_basket_schema: CreateBasketBrokerSchema) -> None:
        await self._service.create_basket(create_basket_schema.basket_id)
