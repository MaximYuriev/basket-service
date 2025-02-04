from dishka.integrations.faststream import inject, FromDishka
from faststream.rabbit import RabbitRouter

from src.broker.basket.adapter import FromBrokerToBasketServiceAdapter
from src.broker.basket.schemas import CreateBasketBrokerSchema

basket_router = RabbitRouter(prefix="basket-")


@basket_router.subscriber("create", exchange="user")
@inject
async def create_product(
        basket_schema: CreateBasketBrokerSchema,
        basket_adapter: FromDishka[FromBrokerToBasketServiceAdapter],
) -> None:
    await basket_adapter.create_basket(basket_schema)
