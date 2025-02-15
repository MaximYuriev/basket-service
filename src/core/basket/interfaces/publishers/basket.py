import uuid
from abc import ABC, abstractmethod

from src.core.basket.entities.basket import Basket


class IBasketPublisher(ABC):
    @abstractmethod
    async def purchase_products(self, basket: Basket, order_id: uuid.UUID) -> None:
        pass

    @abstractmethod
    async def cancel_order(self, order_id: uuid.UUID, reason: str = "") -> None:
        pass
