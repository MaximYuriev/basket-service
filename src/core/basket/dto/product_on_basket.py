from dataclasses import dataclass


@dataclass
class AddProductOnBasketDTO:
    product_id: int
    quantity_on_basket: int
    marked_for_order: bool


@dataclass
class UpdateProductOnBasketDTO:
    product_id: int
    quantity_on_basket: int | None = None
    marked_for_order: bool | None = None
