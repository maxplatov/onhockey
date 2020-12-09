"""Класс для работы с данными сайта."""
__author__ = 'Платов М.И.'

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

    def __init__(self, token: str, parse_mode: str):
        self.games: List[Game] = []
        super().__init__(token, parse_mode=parse_mode)

    async def refresh_games(self):
        """Обновляем данные о текущих играх"""
        while True:
            self.games = []
            for item in await get_games():
                game = Game(*item)
                await game.async_init()
                self.games.append(game)
            await asyncio.sleep(SYNC_PERIOD)

    async def get_sought_game(self, team: str, user_id: int) -> Optional[Game]:
        """
        Получить игру по названию команды
        Args:
            team: Название команды
            user_id: Ид пользователя делающего запрос

        Returns:
            Игра с ссылками на трансляцию
        """
        eng_team_name = get_team_name(team)
        asyncio.create_task(register_request(user_id, eng_team_name))
        if self.games:
            team_name = eng_team_name.split(' ')[0].lower()
            for game in self.games:
                if team_name in game:
                    return game
        return None

    async def on_startup(self, dispatcher: Dispatcher):
        """Хук старта приложения."""
        # TODO: need use alembic migrations
        await create_db()
        asyncio.create_task(self.refresh_games())

    def run(self, dispatcher: Dispatcher):
        """Запуск бота."""
        asyncio.run(executor.start_polling(dispatcher, on_startup=self.on_startup))
