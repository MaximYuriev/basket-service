from typing import AsyncIterable

from dishka import Provider, from_context, Scope, provide
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from src.api.basket.adapter import BasketServiceAdapter
from src.config import Config
from src.core.basket.interfaces.repositories.basket import IBasketRepository
from src.core.basket.repositories.basket import BasketRepository
from src.core.basket.services.basket import BasketService


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


class AppProvider(Provider):
    basket_repository = provide(BasketRepository, scope=Scope.REQUEST, provides=IBasketRepository)
    basket_service = provide(BasketService, scope=Scope.REQUEST)
    basket_service_adapter = provide(BasketServiceAdapter, scope=Scope.REQUEST)
