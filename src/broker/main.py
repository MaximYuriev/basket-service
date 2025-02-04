from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.broker.basket.consumer import basket_router
from src.config import Config
from src.broker.product.consumer import product_router
from src.ioc import ProductProvider, SQLAlchemyProvider, BasketProvider
from src.main import config

container = make_async_container(
    BasketProvider(),
    ProductProvider(),
    SQLAlchemyProvider(),
    context={Config: config},
)

broker = RabbitBroker(url=config.rmq.rmq_url)
app = FastStream(broker)
broker.include_routers(product_router)
broker.include_routers(basket_router)

setup_dishka(container, app)
