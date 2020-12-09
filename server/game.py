"""Класс - Матч двух команд"""
__author__ = 'Платов М.И.'

import logging
from dataclasses import dataclass
from typing import List

import asyncio

from server.data_requests import get_source_link
from server.gino.operations import create_team_if_not_exist

log = logging.getLogger(__name__)


def _get_teams(info: str) -> List[str]:
    """Парсинг строки с названиями команд"""
    return info.split('-')


@dataclass()
class Game:
    """Игра с трансляциями"""
    info: str
    channels: List[str]

    def __contains__(self, team: str):
        """Перегрузка вхождения"""
        item = team.lower()
        return item in self.home.lower() or item in self.guest.lower() or item in self.info.lower()

    def __post_init__(self):
        self.links: List[str] = []
        home, guest = _get_teams(self.info)
        self.home: str = home
        self.guest: str = guest

    async def async_init(self):
        """Запускает фоновые задачи по поиску ссылок на трансляции"""
        await self.get_link_from_channel()
        await self.registry_teams()

    async def registry_teams(self):
        """Записывает в базу название команды"""
        await create_team_if_not_exist(self.home)
        await create_team_if_not_exist(self.guest)

    async def get_link_from_channel(self):
        """Добавляет ссылку на прямую трансляцию из канала"""
        futures = [get_source_link(channel) for channel in self.channels]
        for res in await asyncio.gather(*futures, return_exceptions=True):
            if isinstance(res, Exception):
                log.info(res)
            elif res:
                self.links.append(res)
