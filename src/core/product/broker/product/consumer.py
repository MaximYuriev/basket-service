from dishka.integrations.faststream import inject, FromDishka
from faststream.rabbit import RabbitRouter

from src.core.product.broker.product.adapter import FromBrokerToProductServiceAdapter
from src.core.product.broker.product.schemas import UpdateProductBrokerSchema, CreateProductBrokerSchema, \
    DeleteProductBrokerSchema
from src.core.product.exceptions.product import ProductNotFoundException

product_router = RabbitRouter(prefix="product-")


@product_router.subscriber("create", exchange="product")
@inject
async def create_product(
        product_schema: CreateProductBrokerSchema,
        product_adapter: FromDishka[FromBrokerToProductServiceAdapter],
) -> None:
    await product_adapter.create_product(product_schema)


@product_router.subscriber("update", exchange="product")
@inject
async def update_product(
        product_schema: UpdateProductBrokerSchema,
        product_adapter: FromDishka[FromBrokerToProductServiceAdapter],
) -> None:
    try:
        await product_adapter.update_product(product_schema)
    except ProductNotFoundException as exc:
        print(exc.message)


@product_router.subscriber("delete", exchange="product")
@inject
async def create_product(
        product_schema: DeleteProductBrokerSchema,
        product_adapter: FromDishka[FromBrokerToProductServiceAdapter],
) -> None:
    try:
        await product_adapter.delete_product(product_schema)
    except ProductNotFoundException as exc:
        print(exc.message)
