from app.orm.models import Team
from app.managers.base import BaseManager
from app.schemes import TeamCreate


class TeamManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(Team, *args, **kwargs)

    async def create(self, model: TeamCreate) -> Team:
        return await self.insert(Team(**model.dict()))

    async def select_team(self, team_name: str) -> int:
        team_name = team_name.strip()
        result = await self.exec(
            self.select.where(Team.name == team_name)
        )
        return result and result.scalars().one()

    async def create_team_if_not_exist(self, team_name: str) -> int:
        team_id = await self.select_team(team_name)
        if not team_id:
            return (await self.create(TeamCreate(name=team_name.strip()))).id
        return team_id
