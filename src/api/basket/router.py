import uuid
from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Depends

from authorizer.http.dependencies import get_user_id_from_token
from src.api.basket.adapter import BasketServiceAdapter
from src.api.basket.exceptions.basket import HTTPBasketNotFoundException
from src.api.basket.exceptions.product import HTTPProductNotFoundException, HTTPProductAlreadyInBasketException
from src.api.basket.response import BasketResponse
from src.api.basket.schemas.product import AddProductSchema, UpdateProductSchema
from src.core.basket.exceptions.basket import BasketNotFoundException
from src.core.basket.exceptions.product_on_basket import ProductOnBasketNotFoundException, \
    ProductAlreadyInBasketException
from src.core.product.exceptions.product import ProductNotFoundException

basket_router = APIRouter(prefix="/basket", tags=["Basket"])


@basket_router.post("")
@inject
async def add_product_on_basket(
        basket_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
        create_product_schema: AddProductSchema,
        basket_service_adapter: FromDishka[BasketServiceAdapter],
) -> BasketResponse:
    try:
        await basket_service_adapter.add_product_on_basket(basket_id, create_product_schema)
    except BasketNotFoundException as exc:
        raise HTTPBasketNotFoundException(exc.message)
    except ProductNotFoundException as exc:
        raise HTTPProductNotFoundException(exc.message)
    except ProductAlreadyInBasketException as exc:
        raise HTTPProductAlreadyInBasketException(exc.message)
    else:
        return BasketResponse(detail="Товар успешно добавлен!")


@basket_router.get("")
@inject
async def get_basket(
        basket_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
        basket_service_adapter: FromDishka[BasketServiceAdapter],
) -> BasketResponse:
    try:
        basket = await basket_service_adapter.get_basket(basket_id)
    except BasketNotFoundException as exc:
        raise HTTPBasketNotFoundException(exc.message)
    else:
        return BasketResponse(detail="Корзина успешно найдена!", data=basket)


@basket_router.patch("/{product_id}")
@inject
async def update_product_on_basket(
        basket_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
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


@basket_router.delete("/{product_id}")
@inject
async def remove_product_from_basket(
        basket_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
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
