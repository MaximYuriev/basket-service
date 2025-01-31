from dataclasses import dataclass


@dataclass
class AddProductDTO:
    product_id: int
    quantity_on_basket: int
    marked_for_order: bool


@dataclass
class UpdateProductDTO:
    product_id: int
    quantity_on_basket: int | None = None
    marked_for_order: bool | None = None
