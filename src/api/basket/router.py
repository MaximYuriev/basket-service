import uuid

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter

from src.api.basket.adapter import BasketServiceAdapter
from src.api.basket.exceptions.basket import HTTPBasketAlreadyExistException, HTTPBasketNotFoundException
from src.api.basket.exceptions.product import HTTPProductNotFoundException, HTTPProductAlreadyInBasketException
from src.api.basket.response import BasketResponse
from src.api.basket.schemas.basket import CreateBasketSchema
from src.api.basket.schemas.product import AddProductSchema, UpdateProductSchema
from src.core.basket.exceptions.basket import BasketAlreadyExistException, BasketNotFoundException
from src.core.basket.exceptions.product_on_basket import ProductOnBasketNotFoundException, ProductAlreadyInBasketException

basket_router = APIRouter(prefix="/basket", tags=["Basket"])


@basket_router.post("/add/basket")
@inject
async def create_basket(
        create_basket_schema: CreateBasketSchema,
        basket_service_adapter: FromDishka[BasketServiceAdapter],
) -> BasketResponse:
    try:
        await basket_service_adapter.create_basket(create_basket_schema)
    except BasketAlreadyExistException as exc:
        raise HTTPBasketAlreadyExistException(exc.message)
    else:
        return BasketResponse(detail="Корзина успешно создана!")


@basket_router.post("/add/product/{basket_id}")
@inject
async def add_product_on_basket(
        basket_id: uuid.UUID,
        create_product_schema: AddProductSchema,
        basket_service_adapter: FromDishka[BasketServiceAdapter],
) -> BasketResponse:
    try:
        await basket_service_adapter.add_product_on_basket(basket_id, create_product_schema)
    except BasketNotFoundException as exc:
        raise HTTPBasketNotFoundException(exc.message)
    except ProductOnBasketNotFoundException as exc:
        raise HTTPProductNotFoundException(exc.message)
    except ProductAlreadyInBasketException as exc:
        raise HTTPProductAlreadyInBasketException(exc.message)
    else:
        return BasketResponse(detail="Товар успешно добавлен!")


@basket_router.get("/{basket_id}")
@inject
async def get_basket(
        basket_id: uuid.UUID,
        basket_service_adapter: FromDishka[BasketServiceAdapter],
) -> BasketResponse:
    try:
        basket = await basket_service_adapter.get_basket(basket_id)
    except BasketNotFoundException as exc:
        raise HTTPBasketNotFoundException(exc.message)
    else:
        return BasketResponse(detail="Корзина успешно найдена!", data=basket)


@basket_router.patch("/update/product/{basket_id}")
@inject
async def update_product_on_basket(
        basket_id: uuid.UUID,
        product_id: int,
        update_product_schema: UpdateProductSchema,
        basket_service_adapter: FromDishka[BasketServiceAdapter],
) -> BasketResponse:
    try:
        await basket_service_adapter.update_product_on_basket(basket_id, product_id, update_product_schema)
    except ProductOnBasketNotFoundException as exc:
        HTTPProductNotFoundException(exc.message)
    except BasketNotFoundException as exc:
        HTTPBasketNotFoundException(exc.message)
    else:
        return BasketResponse(detail="Товар успешно изменен!")


@basket_router.delete("/remove/product/{basket_id}")
@inject
async def remove_product_from_basket(
        basket_id: uuid.UUID,
        product_id: int,
        basket_service_adapter: FromDishka[BasketServiceAdapter],
) -> BasketResponse:
    try:
        await basket_service_adapter.remove_product_from_basket(basket_id, product_id)
    except BasketNotFoundException as exc:
        raise HTTPBasketNotFoundException(exc.message)
    except ProductOnBasketNotFoundException as exc:
        raise HTTPProductNotFoundException(exc.message)
    else:
        return BasketResponse(detail="Товар успешно удален!")
