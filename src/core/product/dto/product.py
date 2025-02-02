from dataclasses import dataclass


@dataclass
class UpdateProductDTO:
    product_name: str | None = None
    price_per_piece: int | None = None
