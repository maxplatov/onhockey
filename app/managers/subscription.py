from typing import List
from sqlalchemy import func, select, join

from app.orm.models import Subscription, Team
from app.managers.base import BaseManager
from app.schemes import SubscriptionCreate


class SubscriptionManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(Subscription, *args, **kwargs)

    async def create(self, model: SubscriptionCreate) -> Subscription:
        return await self.insert(SubscriptionCreate(**model.dict()))

    async def get_subscribers(self, teams: List[str]) -> List[int]:
        teams = [x.strip() for x in teams]
        stmt = select([
            func.array_agg(
                func.distinct(Subscription.user_id)
            )
        ]).join(
            Team
        ).where(
            Team.name.in_(teams)
        )
        return await self.get_all(stmt)

    async def get_teams(self, user_id: int) -> List[str]:
        stmt = select([
            func.array_agg(Team.name)
        ]).select_from(
            join(Subscription, Team)
        ).where(
            Subscription.user_id == user_id
        )
        result = await self.exec(stmt)
        if result:
            return result.scalars().one()
        return []

    async def clear(self, user_id: int):
        await self.exec(self.select.where(Subscription.user_id == user_id).delete())
