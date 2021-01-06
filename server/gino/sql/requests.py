"""Запросы в таблицу requests"""
__author__ = 'Платов М.И.'

from server.gino.models.requests import Requests
from server.gino.sql.teams import select_team


async def register_request(user_id: int, team_name: str):
    """
    Фиксирует запрос пользователя
    Args:
        user_id: Id пользователя
        team_name: Название команды, которую искал пользователь
    """
    team_id = await select_team(team_name)
    if team_id:
        await Requests.create(user_id=user_id, team_id=team_id)
