from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.config import Config
from src.core.product.broker.product.consumer import product_router
from src.ioc import ProductProvider, SQLAlchemyProvider
from src.main import config

container = make_async_container(ProductProvider(), SQLAlchemyProvider(), context={Config: config})

broker = RabbitBroker(url=config.rmq.rmq_url)
faststream_app = FastStream(broker)
broker.include_routers(product_router)

setup_dishka(container, faststream_app)
