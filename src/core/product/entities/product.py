from dataclasses import dataclass


@dataclass
class Product:
    product_id: int
    product_name: str
    price_per_piece: int
