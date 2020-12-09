"""Взаимодействие с базой данных"""
__author__ = 'Платов М.И.'

from typing import List

from server.gino.models import db
from server.gino.models.teams import Teams
from server.gino.models.requests import Requests
from common.constants import TOP_LIMIT


async def create_team_if_not_exist(team_name: str):
    """
    Создаёт команду в базе, если её там нет.
    Args:
        team_name: Имя команды
    Returns:
        PK
    """
    team_name = team_name.strip()
    team_id = await Teams.select('id').where(Teams.name == team_name).gino.scalar()
    if not team_id:
        return (await Teams.create(name=team_name)).id
    return team_id


async def register_request(user_id: int, team_name: str):
    """
    Фиксирует запрос пользователя
    Args:
        user_id: Id пользователя
        team_name: Название команды, которую искал пользователь
    """
    await Requests.create(user_id=user_id, team_id=await create_team_if_not_exist(team_name))


async def top_request_team(limit: int = TOP_LIMIT) -> List[str]:
    """
    Список самых популярных команд
    Args:
        limit: Количество выводимых команд

    Returns:
        Отсортированный по популярности массив названий команд.
    """
    teams = await db.select([
        Teams.name,
        db.func.count(Teams.id).label("count_resp")
    ]).select_from(
        Requests.outerjoin(Teams)
    ).group_by(
        Teams.id
    ).order_by(
        db.text('"count_resp" DESC')
    ).limit(
        limit
    ).gino.all()
    return [x for x, y in teams]
