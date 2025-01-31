from src.api.base.response import BaseResponse
from src.api.basket.schemas.basket import BasketSchema


class BasketResponse(BaseResponse):
    data: BasketSchema | None = None
