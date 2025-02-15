from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.broker.basket.consumer import basket_router
from src.broker.order.consumer import order_router
from src.broker.product.consumer import product_router
from src.main import config, container

broker = RabbitBroker(url=config.rmq.rmq_url)
app = FastStream(broker)
broker.include_routers(product_router)
broker.include_routers(basket_router)
broker.include_routers(order_router)

setup_dishka(container, app)
