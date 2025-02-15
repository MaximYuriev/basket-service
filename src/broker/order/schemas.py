import uuid
from abc import ABC

from pydantic import BaseModel


class OrderBrokerSchema(BaseModel, ABC):
    pass


class PrepareOrderBrokerSchema(OrderBrokerSchema):
    basket_id: uuid.UUID
    order_id: uuid.UUID
