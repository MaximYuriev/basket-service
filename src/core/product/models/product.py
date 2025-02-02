from sqlalchemy.orm import mapped_column, Mapped

from src.core.base.model import Base
from src.core.product.entities.product import Product


class ProductModel(Base):
    __tablename__ = "product"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    price_per_piece: Mapped[int]

    @classmethod
    def create_from_entity(cls, product: Product) -> 'ProductModel':
        return cls(
            product_id=product.product_id,
            product_name=product.product_name,
            price_per_piece=product.price_per_piece,
        )
