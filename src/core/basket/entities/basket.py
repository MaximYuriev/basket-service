import uuid
from dataclasses import dataclass, field

from src.core.basket.entities.product_on_basket import ProductOnBasket


@dataclass
class Basket:
    basket_id: uuid.UUID
    products_on_basket: list[ProductOnBasket] = field(default_factory=list)
