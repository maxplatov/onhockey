"""Запросы в таблицу subscriptions"""
__author__ = 'Платов М.И.'

from typing import List

from server.gino.models import db
from server.gino.models.teams import Teams
from server.gino.models.subscriptions import Subscriptions
from server.gino.sql.teams import select_team


async def create_subscribes(team_name: str, user_id: int) -> bool:
    """
    Подписка на команду.
    Args:
        team_name: Название команды
        user_id: ID пользователя

    Returns:
        PK - записи
    """
    team_id = await select_team(team_name)
    if team_id:
        await Subscriptions.create(user_id=user_id, team_id=team_id)
        return True
    return False


async def get_subscribers(teams: List[str]) -> List[int]:
    """
    Список подписчиков для переданных команд
    Args:
        teams: Список команд начинающих играть

    Returns:
        Список пользователей подписавшихся на эти команды.
    """
    teams = [x.strip() for x in teams]
    users = await db.select([
        db.func.array_agg(Subscriptions.user_id)
    ]).select_from(
        Subscriptions.outerjoin(Teams)
    ).where(
        Teams.name.in_(teams)
    ).distinct(
        Subscriptions.user_id
    ).group_by(
        Subscriptions.user_id
    ).gino.scalar()
    return users


async def get_teams(user_id: int) -> List[str]:
    """Список команд на которые подписан пользователь"""
    return (await db.select([
        db.func.array_agg(Teams.name)
    ]).select_from(
        Subscriptions.outerjoin(Teams)
    ).where(
        Subscriptions.user_id == user_id
    ).gino.scalar()) or []


async def clear(user_id: int):
    """Удаление всех подписок"""
    await Subscriptions.delete.where(
        Subscriptions.user_id == user_id
    ).gino.scalar()
