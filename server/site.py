"""Запросы на сайт"""
__author__ = 'Платов М.И.'

from urllib import parse
from typing import List

import requests
from bs4 import BeautifulSoup

from common.constants import SiteInfo, BodyConfig


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


def get_schedule(team: str) -> List[str]:
    """
    Расписание игр для команды
    Args:
        team: Имя команды

    Returns:
        Внутренние пути до трансляций
    """
    parser = BeautifulSoup(_get_responce(SiteInfo.SCHEDULE), 'html.parser')
    games = parser.find('table', BodyConfig.TABLE).find_all('tr', BodyConfig.GAME)
    found_game = None
    links = []
    for game_info in games:
        if team in game_info.text.lower():
            found_game = game_info
            break
    if found_game:
        href_tags = found_game.find_all('a') or []
        for tag in href_tags:
            links.append(tag.get('href'))
    # пользователи хотят ссылки на трансляции, а не файлы
    return list(filter(lambda x: FILE_EXTENSION not in x, links))


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
