"""Сбор всех доступных игр"""
__author__ = 'Платов М.И.'

from typing import List

from server.sources.game import Game
from server.sources.onhockey.data import get_games as get_onhockey_games


async def get_all_games() -> List[Game]:
    """Сбор игр со всех источников."""
    games = []
    games.extend(await get_onhockey_games())
    return games
