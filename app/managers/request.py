from typing import Optional

from app.orm.models import Request, Team
from app.managers.base import BaseManager
from app.schemes import RequestCreate


class RequestManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(Request, *args, **kwargs)

    async def create(self, model: RequestCreate) -> Request:
        return await self.insert(Request(**model.dict()))

    async def register_request(self, user_id: int, team: Optional[Team]):
        await self.create(RequestCreate(user_id=user_id, team_id=team.id if team else None))
