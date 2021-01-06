"""Запросы в таблицу teams"""
__author__ = 'Платов М.И.'

from server.gino.models.teams import Teams


async def select_team(team_name: str) -> int:
    """Поиск команды по названию"""
    team_name = team_name.strip()
    return await Teams.select('id').where(Teams.name == team_name).gino.scalar()


async def create_team_if_not_exist(team_name: str) -> int:
    """
    Создаёт команду в базе, если её там нет.
    Args:
        team_name: Имя команды
    Returns:
        PK
    """
    team_id = await select_team(team_name)
    if not team_id:
        return (await Teams.create(name=team_name.strip())).id
    return team_id
