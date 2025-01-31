from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str
    data: None
