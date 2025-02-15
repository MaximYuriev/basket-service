import uuid

from sqlalchemy import select, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, with_loader_criteria

from src.core.basket.dto.product_on_basket import AddProductOnBasketDTO, ProductOnBasketFilter
from src.core.basket.entities.basket import Basket
from src.core.basket.entities.product_on_basket import ProductOnBasket
from src.core.basket.exceptions.basket import BasketNotFoundException, BasketAlreadyExistException
from src.core.basket.exceptions.product_on_basket import ProductOnBasketNotFoundException
from src.core.basket.interfaces.repositories.basket import IBasketRepository
from src.core.basket.models.basket import BasketModel
from src.core.basket.models.product_on_basket import ProductOnBasketModel
from src.core.product.exceptions.product import ProductNotFoundException


class BasketRepository(IBasketRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_basket_on_db(self, basket: Basket) -> None:
        basket_model = BasketModel.create_from_entity(basket)
        self._session.add(basket_model)
        try:
            await self._session.commit()
        except IntegrityError:
            raise BasketAlreadyExistException

    async def get_basket_by_id(self, basket_id: uuid.UUID, filters: ProductOnBasketFilter | None = None) -> Basket:
        if filters is None:
            basket_model = await self._get_basket_model(basket_id=basket_id)
        else:
            basket_model = await self._get_basket_model_with_product_filter(marked_for_order=filters.marked_for_order,
                                                                            basket_id=basket_id)
        return basket_model.convert_to_entity()

    async def save_product_on_basket(self, product: AddProductOnBasketDTO, basket: Basket) -> None:
        product_model = ProductOnBasketModel.create_from_dto(product, basket)
        self._session.add(product_model)
        try:
            await self._session.commit()
        except IntegrityError:
            raise ProductNotFoundException(product_id=product.product_id)

    async def delete_product_from_basket(self, product_id: int, basket: Basket) -> None:
        product_model = await self._get_product_on_basket_model(
            product_id=product_id,
            basket_id=basket.basket_id,
        )
        await self._session.delete(product_model)
        await self._session.commit()

    async def get_product_from_basket(self, basket: Basket, product_id: int) -> ProductOnBasket:
        product_model = await self._get_product_on_basket_model(
            product_id=product_id,
            basket_id=basket.basket_id,
        )
        return product_model.convert_to_entity()

    async def update_product_on_basket(self, product: ProductOnBasket, basket: Basket) -> None:
        product_model = await self._get_product_on_basket_model(
            product_id=product.product_id,
            basket_id=basket.basket_id,
        )
        for key, value in product.__dict__.items():
            if value != product.product_id:
                setattr(product_model, key, value)
        await self._session.commit()

    async def _get_basket_model_by_query(self, query: Select[tuple[BasketModel]]) -> BasketModel:
        basket_model = await self._session.scalar(query)
        if basket_model is not None:
            return basket_model
        raise BasketNotFoundException

    async def _get_basket_model(self, **kwargs) -> BasketModel:
        query = (
            select(BasketModel)
            .options(
                selectinload(BasketModel.products)
                .joinedload(ProductOnBasketModel.product)
            )
            .filter_by(**kwargs)
        )
        return await self._get_basket_model_by_query(query)

    async def _get_basket_model_with_product_filter(self, marked_for_order: bool, **kwargs) -> BasketModel:
        query = (
            select(BasketModel)
            .options(
                selectinload(BasketModel.products)
                .joinedload(ProductOnBasketModel.product),
                with_loader_criteria(
                    ProductOnBasketModel,
                    ProductOnBasketModel.marked_for_order == marked_for_order,
                )
            )
            .filter_by(**kwargs)
        )
        return await self._get_basket_model_by_query(query)

    async def _get_product_on_basket_model(self, **kwargs) -> ProductOnBasketModel:
        query = (
            select(ProductOnBasketModel)
            .options(joinedload(ProductOnBasketModel.product))
            .filter_by(**kwargs)
        )
        product_model = await self._session.scalar(query)
        if product_model is not None:
            return product_model
        raise ProductOnBasketNotFoundException
