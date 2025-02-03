from typing import AsyncIterable

from dishka import Provider, from_context, Scope, provide
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from src.api.basket.adapter import BasketServiceAdapter
from src.config import Config
from src.core.basket.interfaces.repositories.basket import IBasketRepository
from src.core.basket.repositories.basket import BasketRepository
from src.core.basket.services.basket import BasketService
from src.broker.product.adapter import FromBrokerToProductServiceAdapter
from src.core.product.interfaces.repositories.product import IProductRepository
from src.core.product.repositories.product import ProductRepository
from src.core.product.services.product import ProductService


class SQLAlchemyProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_async_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.postgres.db_url, echo=False)

    @provide(scope=Scope.APP)
    def get_async_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class BasketProvider(Provider):
    scope = Scope.REQUEST

    basket_repository = provide(BasketRepository, provides=IBasketRepository)
    basket_service = provide(BasketService)
    basket_service_adapter = provide(BasketServiceAdapter)


class ProductProvider(Provider):
    scope = Scope.REQUEST

    product_repository = provide(ProductRepository, provides=IProductRepository)
    product_service = provide(ProductService)
    product_service_adapter = provide(FromBrokerToProductServiceAdapter)
