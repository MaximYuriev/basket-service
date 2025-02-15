import uuid

from src.core.basket.dto.product_on_basket import UpdateProductOnBasketDTO, AddProductOnBasketDTO, ProductOnBasketFilter
from src.core.basket.entities.basket import Basket
from src.core.basket.entities.product_on_basket import ProductOnBasket
from src.core.basket.exceptions.basket import BasketNotFoundException
from src.core.basket.exceptions.product_on_basket import ProductOnBasketNotFoundException, \
    ProductAlreadyInBasketException
from src.core.basket.interfaces.publishers.basket import IBasketPublisher
from src.core.basket.interfaces.repositories.basket import IBasketRepository


class BasketService:
    def __init__(self, repository: IBasketRepository, publisher: IBasketPublisher):
        self._publisher = publisher
        self._repository = repository

    async def create_basket(self, basket_id: uuid.UUID) -> None:
        basket = Basket(basket_id)
        await self._repository.add_basket_on_db(basket)

    async def get_basket(self, basket_id: uuid.UUID, filters: ProductOnBasketFilter | None = None) -> Basket:
        if filters is None:
            return await self._repository.get_basket_by_id(basket_id)
        return await self._repository.get_basket_by_id(basket_id, filters)

    async def add_product_on_basket(self, product: AddProductOnBasketDTO, basket_id: uuid.UUID) -> None:
        basket = await self.get_basket(basket_id)
        await self._validate_added_product(product, basket)
        await self._repository.save_product_on_basket(product, basket)

    async def remove_product_from_basket(self, product_id: int, basket_id: uuid.UUID) -> None:
        basket = await self.get_basket(basket_id)
        await self._repository.delete_product_from_basket(product_id, basket)

    async def update_product_on_basket(self, update_product: UpdateProductOnBasketDTO, basket_id: uuid.UUID) -> None:
        basket = await self.get_basket(basket_id)
        product_on_basket = await self._get_product_from_basket(basket, update_product.product_id)
        update_product_data = update_product.__dict__
        for key, value in update_product_data.items():
            if value is not None:
                setattr(product_on_basket, key, value)
        await self._repository.update_product_on_basket(product_on_basket, basket)

    async def pay_for_products_in_basket(self, basket_id: uuid.UUID, order_id: uuid.UUID) -> None:
        filters = ProductOnBasketFilter(marked_for_order=True)
        try:
            basket = await self._repository.get_basket_by_id(basket_id, filters=filters)
        except BasketNotFoundException:
            await self._publisher.cancel_order(order_id, reason="Корзина не найдена!")
        else:
            if basket.products_on_basket:
                await self._publisher.purchase_products(basket, order_id)
            else:
                await self._publisher.cancel_order(order_id, reason="В корзине нет товаров!")

    async def _validate_added_product(self, product: AddProductOnBasketDTO, basket: Basket) -> None:
        try:
            await self._get_product_from_basket(basket, product.product_id)
        except ProductOnBasketNotFoundException:
            pass
        else:
            raise ProductAlreadyInBasketException

    async def _get_product_from_basket(self, basket: Basket, product_id: int) -> ProductOnBasket:
        return await self._repository.get_product_from_basket(basket, product_id)
