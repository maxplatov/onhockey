"""Извлечение данных с onhockey.tv"""
__author__ = 'Платов М.И.'

from typing import List

from bs4 import BeautifulSoup

from server.sources.data_requests import get_response
from server.sources.onhockey.constants import SiteInfo
from common.func import get_valid_link, is_vk_link, get_video_from_vk


def get_teams(info: str) -> List[str]:
    """Парсинг строки с названиями команд"""
    return info.split(' - ')


async def get_source_link(channel: str):
    """
    Ссылка на трансляцию
    Args:
        channel: внутренний URL сайта

    Returns:
        Прямая ссылка на трансляцию
    """
    res = await get_response(channel, SiteInfo.ADDRESS)
    link = None
    if res:
        iframe = BeautifulSoup(res, 'html.parser').find('iframe')
        url = iframe and iframe.get('src')
        link = get_valid_link(iframe and iframe.get('src'))
        if not link and is_vk_link(url):
            link = get_video_from_vk(url)
    return link
