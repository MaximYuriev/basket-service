import uuid

from src.core.base.schemas import BrokerPublishedMessage


class ProductToBrokerSchema(BrokerPublishedMessage):
    product_id: int
    quantity_on_basket: int


class PurchaseProductSchema(BrokerPublishedMessage):
    order_id: uuid.UUID
    basket_id: uuid.UUID
    products: list[ProductToBrokerSchema]
