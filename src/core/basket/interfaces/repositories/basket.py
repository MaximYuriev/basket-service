import uuid
from abc import ABC, abstractmethod

from src.core.basket.dto.product_on_basket import AddProductOnBasketDTO
from src.core.basket.entities.basket import Basket
from src.core.basket.entities.product_on_basket import ProductOnBasket


class IBasketRepository(ABC):
    @abstractmethod
    async def add_basket_on_db(self, basket: Basket) -> None: ...

    @abstractmethod
    async def get_basket_by_id(self, basket_id: uuid.UUID) -> Basket: ...

    @abstractmethod
    async def save_product_on_basket(self, product: AddProductOnBasketDTO, basket: Basket) -> None: ...

    @abstractmethod
    async def delete_product_from_basket(self, product_id: int, basket: Basket) -> None: ...

    @abstractmethod
    async def get_product_from_basket(self, basket: Basket, product_id: int) -> ProductOnBasket: ...

    @abstractmethod
    async def update_product_on_basket(self, product: ProductOnBasket, basket: Basket) -> None: ...
