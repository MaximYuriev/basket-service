import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base.model import Base
from src.core.basket.dto.product_on_basket import AddProductDTO
from src.core.basket.entities.basket import Basket
from src.core.basket.entities.product_on_basket import ProductOnBasket
from src.core.basket.models.basket import BasketModel
from src.core.product.models.product import ProductModel


class ProductOnBasketModel(Base):
    __tablename__ = 'product_on_basket'
    product_id: Mapped[int] = mapped_column(ForeignKey(ProductModel.product_id), primary_key=True)
    basket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(BasketModel.basket_id), primary_key=True)
    quantity_on_basket: Mapped[int]
    marked_for_order: Mapped[bool] = mapped_column(default=True)

    product: Mapped["ProductModel"] = relationship()

    @classmethod
    def create_from_dto(cls, product: AddProductDTO, basket: Basket) -> 'ProductOnBasketModel':
        return cls(
            product_id=product.product_id,
            basket_id=basket.basket_id,
            quantity_on_basket=product.quantity_on_basket,
            marked_for_order=product.marked_for_order,
        )

    def convert_to_entity(self) -> ProductOnBasket:
        return ProductOnBasket(
            product_id=self.product_id,
            product_name=self.product.product_name,
            quantity_on_basket=self.quantity_on_basket,
            price_per_piece=self.product.price_per_piece,
            marked_for_order=self.marked_for_order,
        )
