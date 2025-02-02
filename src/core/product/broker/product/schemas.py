from abc import ABC

from pydantic import BaseModel, Field


class ProductBrokerSchema(BaseModel, ABC):
    pass


class CreateProductBrokerSchema(ProductBrokerSchema):
    product_id: int
    name: str = Field(serialization_alias="product_name")
    price: int = Field(serialization_alias="price_per_piece")


class UpdateProductBrokerSchema(ProductBrokerSchema):
    product_id: int = Field(exclude=True)
    name: str | None = Field(default=None, serialization_alias="product_name")
    price: int | None = Field(default=None, serialization_alias="price_per_piece")


class DeleteProductBrokerSchema(ProductBrokerSchema):
    product_id: int
