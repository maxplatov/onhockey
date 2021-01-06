"""Источник данных сайт  - onhockey"""
__author__ = 'Платов М.И.'

import re
from typing import List
from datetime import time

from bs4 import BeautifulSoup

from server.sources.data_requests import get_response
from server.sources.onhockey.onhockey_game import OnHockeyGame
from server.sources.onhockey.constants import SiteInfo, BodyConfig

FILE_EXTENSION = 'm3u8'
"""Расширение файла трансляции"""


def _get_teams_info(game: str) -> str:
    """
    Возвращает строку с названием играющих команд
    Args:
        game: Метаданные игры

    Returns:
        Team 1 - Team 2
    """
    info = re.search(r'([A-Za-z].*-.*)', game)
    return info.group(1) if info else None


def _get_start_info(game: str):
    """
    Время начала игры
    Args:
        game: Метаданные игры

    Returns:
        time(HH, MM)
    """
    info = re.search(r'(..:..)', game)
    if info:
        data = info.group(1).split(':')
        return time(int(data[0]), int(data[1]))
    return None


async def get_games() -> List[OnHockeyGame]:
    """
    Агрегация текущих игр
    Returns:
        Массив игр
    """
    result = []
    res = await get_response(SiteInfo.SCHEDULE, SiteInfo.ADDRESS)
    if res:
        table = BeautifulSoup(res, 'html.parser').find('table', BodyConfig.TABLE)
        if table:
            games = table.find_all('tr', BodyConfig.GAME)
            for game in games:
                channels = []
                info = _get_teams_info(game.text)
                if info:
                    start_time = _get_start_info(game.text)
                    href_tags = game.find_all('a') or []
                    for tag in href_tags:
                        channels.append(tag.get('href'))
                    # пользователи хотят ссылки на трансляции, а не файлы трансляций
                    channels = list(filter(lambda x: FILE_EXTENSION not in x, channels))
                    if channels:
                        result.append(OnHockeyGame(info, start_time, channels))
    return result
