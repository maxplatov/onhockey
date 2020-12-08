"""Класс для работы с данными сайта."""
__author__ = 'Платов М.И.'

import threading
from typing import List, Optional

import asyncio
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from server.game import Game
from server.data_requests import get_games
from server.gino.main import create_db
from server.gino.operations import register_request
from common.func import get_team_name
from common.constants import SYNC_PERIOD


class Onhockey(Bot):
    """Класс Бот - onhockey"""

    games: List[Game] = None

    def __init__(self, token: str, parse_mode: str):
        super().__init__(token, parse_mode=parse_mode)

    def refresh_games(self):
        """Обновляем данные о текущих играх"""
        threading.Timer(SYNC_PERIOD, self.refresh_games).start()
        self.games = []
        for item in get_games():
            self.games.append(Game(*item))

    async def get_sought_game(self, team: str, user_id: int) -> Optional[Game]:
        """
        Получить игру по названию команды
        Args:
            team: Название команды
            user_id: Ид пользователя делающего запрос

        Returns:
            Игра с ссылками на трансляцию
        """
        asyncio.create_task(register_request(user_id, team))
        if self.games:
            eng_team_name = get_team_name(team)
            for game in self.games:
                if eng_team_name in game:
                    return game
        return None

    async def on_startup(self, dispatcher: Dispatcher):
        """Хук старта приложения."""
        await create_db()
        self.refresh_games()

    def run(self, dispatcher: Dispatcher):
        """Запуск бота."""
        executor.start_polling(dispatcher, on_startup=self.on_startup)
