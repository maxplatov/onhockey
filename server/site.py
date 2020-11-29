"""Запросы на сайт"""
__author__ = 'Платов М.И.'

from urllib import parse
from typing import List

import requests
from bs4 import BeautifulSoup

from common.constants import SiteInfo, BodyConfig
from common.func import get_teams_info


FILE_EXTENSION = 'm3u8'
"""Расширение файла трансляции"""


def _get_responce(path: str, site: str = SiteInfo.ADDRESS) -> str:
    """
    Выполнить запрос и получить текст ответа
    Args:
        path: Запрашиваемый путь
        site: Имя сайта

    Returns:
        Текст ответа
    """
    return requests.get(parse.urljoin(site, path)).text


def get_games() -> List[tuple]:
    """
    Агрегация текущих игр
    Returns:
        Массив игр
    """
    parser = BeautifulSoup(_get_responce(SiteInfo.SCHEDULE), 'html.parser')
    games = parser.find('table', BodyConfig.TABLE).find_all('tr', BodyConfig.GAME)
    result = []
    for game in games:
        channels = []
        info = get_teams_info(game.text)
        if info:
            href_tags = game.find_all('a') or []
            for tag in href_tags:
                channels.append(tag.get('href'))
            # пользователи хотят ссылки на трансляции, а не файлы трансляций
            channels = list(filter(lambda x: FILE_EXTENSION not in x, channels))
            if channels:
                result.append((info, channels))
    return result


def get_source_link(channel: str) -> str:
    """
    Ссылка на трансляцию
    Args:
        channel: внутренний URL сайта

    Returns:
        Прямая ссылка на трансляцию
    """
    res = _get_responce(channel)
    iframe = BeautifulSoup(res, 'html.parser').find('iframe')
    return iframe.get('src')
