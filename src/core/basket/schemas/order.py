import uuid

from src.core.base.schemas import BrokerPublishedMessage


class CancelOrderSchema(BrokerPublishedMessage):
    order_id: uuid.UUID
    reason: str
