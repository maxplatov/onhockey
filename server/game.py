"""Класс - Матч двух команд"""
__author__ = 'Платов М.И.'

from dataclasses import dataclass
from typing import List

import asyncio

from server.site import get_source_link


def _get_teams(info: str) -> List[str]:
    """Парсинг строки с названиями команд"""
    return info.lower().split(' - ')


@dataclass()
class Game:
    """Игра с трансляциями"""
    info: str = None
    channels: List[str] = None
    links: List[str] = None

    def __contains__(self, team: str):
        """Перегрузка вхождения"""
        item = team.lower()
        return item in self.home or item in self.guest or item in self.info

    def __post_init__(self):
        self.home, self.guest = _get_teams(self.info)
        futures = [self.get_link_from_channel(channel) for channel in self.channels]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))
        loop.close()

    async def get_link_from_channel(self, channel):
        """
        Добавляет ссылку на прямую трансляцию из канала
        Args:
            channel: Канал, из которого получаем ссылку
        """
        self.links.append(get_source_link(channel))
