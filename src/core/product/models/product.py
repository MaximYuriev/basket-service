from sqlalchemy.orm import mapped_column, Mapped

from src.core.base.model import Base


class ProductModel(Base):
    __tablename__ = "product"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    price_per_piece: Mapped[int]
