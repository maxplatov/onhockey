"""Класс - Матч двух команд"""
__author__ = 'Платов М.И.'

from abc import ABC, abstractmethod
from datetime import time
from typing import List

from server.gino.sql.teams import create_team_if_not_exist


class Game(ABC):
    """Игра с трансляциями"""

    def __init__(self, home: str, guest: str, start_time: time):
        self.home = home
        self.guest = guest
        self.start_time = start_time
        self.links: List[str] = []

    def __contains__(self, team: str):
        """Перегрузка вхождения"""
        item = team.lower()
        return item in self.home.lower() or item in self.guest.lower()

    async def async_init(self):
        """Запускает фоновые задачи по поиску ссылок на трансляции"""
        await self.get_links()
        await self.registry_teams()

    async def registry_teams(self):
        """Записывает в базу название команды"""
        await create_team_if_not_exist(self.home)
        await create_team_if_not_exist(self.guest)

    @abstractmethod
    async def get_links(self):
        """Наполнение игры ссылками"""
        raise NotImplementedError('get_links: method is not implemented')
