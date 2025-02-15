from dishka.integrations.faststream import inject, FromDishka
from faststream.rabbit import RabbitRouter

from src.broker.order.adapter import FromOrderConsumerToBasketServiceAdapter
from src.broker.order.schemas import PrepareOrderBrokerSchema

order_router = RabbitRouter()
publisher = order_router.publisher(exchange="order", queue="order-make")


@order_router.subscriber(exchange="order", queue="order-prepare")
@inject
async def prepare_product_in_basket_for_order(
        order_schema: PrepareOrderBrokerSchema,
        order_adapter: FromDishka[FromOrderConsumerToBasketServiceAdapter],
):
    await order_adapter.pay_for_products_in_basket(order_schema)
