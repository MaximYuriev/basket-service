import uuid

from aio_pika import RobustExchange, RobustQueue
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
from watchfiles import awatch

from src.core.base.schemas import BrokerPublishedMessage
from src.core.basket.entities.basket import Basket
from src.core.basket.interfaces.publishers.basket import IBasketPublisher
from src.core.basket.schemas.order import CancelOrderSchema
from src.core.basket.schemas.product import PurchaseProductSchema, ProductToBrokerSchema


class BasketPublisher(IBasketPublisher):
    _PRODUCT_EXCHANGE_NAME = "product"
    _ORDER_EXCHANGE_NAME = "order"
    _PURCHASE_PRODUCTS_QUEUE_NAME = "product-purchase"
    _CANCEL_ORDER_QUEUE_NAME = "order-cancel"

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def purchase_products(self, basket: Basket, order_id: uuid.UUID) -> None:
        message = PurchaseProductSchema(
            basket_id=basket.basket_id,
            order_id=order_id,
            products=[ProductToBrokerSchema.model_validate(product, from_attributes=True) for product in
                      basket.products_on_basket],
        )
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._PRODUCT_EXCHANGE_NAME,
            queue_name=self._PURCHASE_PRODUCTS_QUEUE_NAME,
        )
        await self._publish(exchange=exchange, queue=queue, message=message)

    async def cancel_order(self, order_id: uuid.UUID, reason: str = "") -> None:
        message = CancelOrderSchema(
            order_id=order_id,
            reason=reason,
        )
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._ORDER_EXCHANGE_NAME,
            queue_name=self._CANCEL_ORDER_QUEUE_NAME,
        )
        await self._publish(exchange=exchange, queue=queue, message=message)

    async def _prepare_to_publish(self, exchange_name: str, queue_name: str) -> tuple[RobustExchange, RobustQueue]:
        exchange = await self._declare_exchange(exchange_name)
        queue = await self._declare_queue(queue_name)
        await self._bind_queue_to_exchange(exchange, queue)
        return exchange, queue

    async def _publish(
            self,
            exchange: RobustExchange,
            queue: RobustQueue,
            message: BrokerPublishedMessage,
    ) -> None:
        await self._broker.publish(
            message=message,
            exchange=exchange.name,
            routing_key=queue.name,
        )

    async def _declare_exchange(self, exchange_name: str) -> RobustExchange:
        exchange = RabbitExchange(exchange_name)
        return await self._broker.declare_exchange(exchange)

    async def _declare_queue(self, queue_name: str) -> RobustQueue:
        queue = RabbitQueue(queue_name)
        return await self._broker.declare_queue(queue)

    @staticmethod
    async def _bind_queue_to_exchange(exchange: RobustExchange, queue: RobustQueue) -> None:
        await queue.bind(
            exchange=exchange.name,
            routing_key=queue.name,
        )
