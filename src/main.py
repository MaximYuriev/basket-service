from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.basket.router import basket_router
from src.config import Config
from src.ioc import AppProvider

config = Config()
container = make_async_container(AppProvider(), context={Config: config})

app = FastAPI(title="Product Service")
app.include_router(basket_router)

setup_dishka(container, app)
