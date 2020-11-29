"""Класс - Матч двух команд"""
__author__ = 'Платов М.И.'

from dataclasses import dataclass
from typing import List

import asyncio

from server.site import get_source_link


def _get_teams(info: str) -> List[str]:
    """Парсинг строки с названиями команд"""
    return info.split(' - ')


@dataclass()
class Game:
    """Игра с трансляциями"""
    info: str = None
    channels: List[str] = None
    links: List[str] = None

    def __contains__(self, team: str):
        """Перегрузка вхождения"""
        item = team.lower()
        return item in self.home.lower() or item in self.guest.lower() or item in self.info.lower()

    def __post_init__(self):
        self.home, self.guest = _get_teams(self.info)
        self.links = []

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_link_from_channel())

    async def get_link_from_channel(self):
        """
        Добавляет ссылку на прямую трансляцию из канала
        """
        futures = [get_source_link(channel) for channel in self.channels]
        done, pending = await asyncio.wait(futures)
        for task in done:
            link = task.result()
            if link:
                self.links.append(link)
