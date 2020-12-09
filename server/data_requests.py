"""Запросы на сайт"""
__author__ = 'Платов М.И.'

from urllib import parse
from typing import List

import aiohttp
from bs4 import BeautifulSoup

from common.constants import SiteInfo, BodyConfig
from common.func import get_teams_info, get_valid_link


FILE_EXTENSION = 'm3u8'
"""Расширение файла трансляции"""


async def _get_response(path: str, site: str = SiteInfo.ADDRESS) -> str:
    """
    Выполнить запрос и получить текст ответа
    Args:
        path: Запрашиваемый путь
        site: Имя сайта

    Returns:
        Текст ответа
    """
    session = aiohttp.ClientSession()
    try:
        async with session.get(parse.urljoin(site, path), raise_for_status=True) as resp:
            if resp.status == 200:
                result = await resp.text()
    except:
        result = ''
    finally:
        await session.close()
    return result


async def get_games() -> List[tuple]:
    """
    Агрегация текущих игр
    Returns:
        Массив игр
    """
    result = []
    res = await _get_response(SiteInfo.SCHEDULE)
    if res:
        table = BeautifulSoup(res, 'html.parser').find('table', BodyConfig.TABLE)
        if table:
            games = table.find_all('tr', BodyConfig.GAME)
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


async def get_source_link(channel: str) -> str:
    """
    Ссылка на трансляцию
    Args:
        channel: внутренний URL сайта

    Returns:
        Прямая ссылка на трансляцию
    """
    res = await _get_response(channel)
    link = None
    if res:
        iframe = BeautifulSoup(res, 'html.parser').find('iframe')
        link = get_valid_link(iframe and iframe.get('src'))
    return link
