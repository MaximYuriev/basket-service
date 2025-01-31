import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base.model import Base
from src.core.basket.entities.basket import Basket


class BasketModel(Base):
    __tablename__ = "basket"
    basket_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)

    products: Mapped[list["ProductOnBasketModel"]] = relationship()

    @classmethod
    def create_from_entity(cls, basket: Basket) -> 'BasketModel':
        return cls(
            basket_id=basket.basket_id,
        )

    def convert_to_entity(self) -> Basket:
        return Basket(
            basket_id=self.basket_id,
            products_on_basket=[product.convert_to_entity() for product in self.products],
        )
