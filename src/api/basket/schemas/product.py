from abc import ABC

from pydantic import BaseModel, Field


class ProductSchema(BaseModel, ABC):
    pass


class OuterProductSchema(ProductSchema):
    product_id: int
    product_name: str
    quantity_on_basket: int
    price_per_piece: int
    marked_for_order: bool


class AddProductSchema(ProductSchema):
    product_id: int
    quantity_on_basket: int = Field(ge=1, le=20)
    marked_for_order: bool = Field(default=True)


class UpdateProductSchema(ProductSchema):
    quantity_on_basket: int | None = Field(default=None, ge=1, le=20)
    marked_for_order: bool | None = None
