import uuid

from pydantic import BaseModel

from src.api.basket.schemas.product import OuterProductSchema


class BaseBasketSchema(BaseModel):
    basket_id: uuid.UUID


class BasketSchema(BaseBasketSchema):
    products_on_basket: list[OuterProductSchema]


class CreateBasketSchema(BaseBasketSchema):
    pass
