"""Класс - Матч двух команд"""
__author__ = 'Платов М.И.'

from dataclasses import dataclass
from typing import List

import asyncio

from server.data_requests import get_source_link
from server.gino.operations import create_team_if_not_exist


def _get_teams(info: str) -> List[str]:
    """Парсинг строки с названиями команд"""
    return info.split(' - ')


@dataclass()
class Game:
    """Игра с трансляциями"""
    info: str = None
    channels: List[str] = None

    links: List[str] = None
    home: str = None
    guest: str = None

    def __contains__(self, team: str):
        """Перегрузка вхождения"""
        item = team.lower()
        return item in self.home.lower() or item in self.guest.lower() or item in self.info.lower()

    def __post_init__(self):
        self.home, self.guest = _get_teams(self.info)
        asyncio.create_task(create_team_if_not_exist(self.home))
        asyncio.create_task(create_team_if_not_exist(self.guest))
        self.links = []

        asyncio.create_task(self.get_link_from_channel())

    async def get_link_from_channel(self):
        """
        Добавляет ссылку на прямую трансляцию из канала
        """
        futures = [get_source_link(channel) for channel in self.channels]
        done, _ = await asyncio.wait(futures)
        for task in done:
            link = task.result()
            if link:
                self.links.append(link)
