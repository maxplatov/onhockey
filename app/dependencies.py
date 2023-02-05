from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.engine import async_session_maker
from app.managers import TeamManager, RequestManager, SubscriptionManager


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_team_manager(session: AsyncSession = Depends(get_async_session)):
    yield TeamManager(session)


async def get_request_manager(session: AsyncSession = Depends(get_async_session)):
    yield RequestManager(session)


async def get_subscription_manager(session: AsyncSession = Depends(get_async_session)):
    yield SubscriptionManager(session)
