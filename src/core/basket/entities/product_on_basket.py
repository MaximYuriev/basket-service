from dataclasses import dataclass


@dataclass
class ProductOnBasket:
    product_id: int
    product_name: str
    quantity_on_basket: int
    price_per_piece: int
    marked_for_order: bool
