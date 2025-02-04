import uuid
from abc import ABC

from pydantic import BaseModel


class BasketBrokerSchema(BaseModel, ABC):
    pass


class CreateBasketBrokerSchema(BasketBrokerSchema):
    basket_id: uuid.UUID
