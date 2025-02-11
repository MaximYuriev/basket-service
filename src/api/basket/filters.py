from pydantic import BaseModel, Field


class ProductOnBasketFilterSchema(BaseModel):
    with_products_marked_for_order: bool | None = Field(default=None, serialization_alias="marked_for_order")
