"""Запросы на сайты"""
__author__ = 'Платов М.И.'

from urllib import parse

import aiohttp


async def get_response(path: str, site: str) -> str:
    """
    Выполнить запрос и получить текст ответа
    Args:
        path: Запрашиваемый путь
        site: Имя сайта

    Returns:
        Текст ответа
    """
    headers = {
        "accept": "*/*",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "referer": site,
    }
    session = aiohttp.ClientSession(headers=headers)
    try:
        async with session.get(parse.urljoin(site, path), raise_for_status=True) as resp:
            if resp.status == 200:
                result = await resp.text()
    except:
        result = ''
    finally:
        await session.close()
    return result
