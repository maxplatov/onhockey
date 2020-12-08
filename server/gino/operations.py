"""Взаимодействие с базой данных"""
__author__ = 'Платов М.И.'

from typing import Optional, List

from server.gino.models import db
from server.gino.models.teams import Teams
from server.gino.models.requests import Requests
from common.constants import TOP_LIMIT


async def __get_team_id(name: str) -> Optional[int]:
    """
    Возвращает первичный ключ по имени команды
    Args:
        name: Название команды

    Returns: PK
    """
    return await Teams.select('id').where(Teams.name == name).gino.scalar()


async def create_team_if_not_exist(team_name: str):
    """
    Создаёт команду в базе, если её там нет.
    Args:
        team_name: Имя команды
    """
    team_id = await __get_team_id(team_name)
    if not team_id:
        await Teams.create(name=team_name)


async def get_team_id(team_name: str) -> int:
    """
    Возвращает идентификатор команды (создаёт команду, если её нет)
    Args:
        team_name: Название команды
    Returns:
        PK
    """
    team_id = await __get_team_id(team_name)
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
    await Requests.create(user_id=user_id, team_id=await get_team_id(team_name))


async def top_request_team(limit: int = TOP_LIMIT) -> List[str]:
    """
    Список самых популярных команд
    Args:
        limit: Количество выводимых команд

    Returns:
        Отсортированный по популярности массив названий команд.
    """
    records = await db.select([
        Teams.name,
        db.func.count(Teams.id)
    ]).select_from(
        Requests.outerjoin(Teams)
    ).group_by(
        Teams.id
    ).gino.all()
    records.sort(key=lambda tup: tup[1], reverse=True)
    return [team for team, count in records[:min(limit, len(records))]]
