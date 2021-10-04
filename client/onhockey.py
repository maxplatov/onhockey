"""Класс для работы с данными сайта."""
__author__ = 'Платов М.И.'

from datetime import datetime, date
from typing import List, Optional

import asyncio
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions as aiogram_exceptions

from server.sources.game import Game
from server.games import get_all_games
from server.gino.main import create_db
from server.gino.sql.requests import register_request
from server.gino.sql.subscriptions import get_subscribers, clear
from common.func import get_team_name, get_button_markup, get_formatted_info, escape_telegram_char
from common.constants import SYNC_PERIOD, UserMessage


class Onhockey(Bot):
    """Класс Бот - onhockey"""

    def __init__(self, token: str, parse_mode: str):
        self.games: List[Game] = []
        super().__init__(token, parse_mode=parse_mode)

    async def refresh_games(self):
        """Обновляем данные о текущих играх"""
        while True:
            self.games = []
            for game in await get_all_games():
                await game.async_init()
                await self.notify_users(game)
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

    async def _notify(self, game: Game):
        """Рассылка сообщений подписчикам."""
        users = await get_subscribers([game.home, game.guest])
        if users:
            markup = get_button_markup(game.links)
            message = UserMessage.START_GAME + get_formatted_info(game)
            for user in users:
                await self.send_escaped_message(
                    user,
                    message,
                    reply_markup=markup
                )

    async def notify_users(self, game: Game):
        """
        Нотификация подписчиков о старте игры
        Args:
            game: Начинающийся матч

        Returns:
            Сообщения подписантам
        """
        today = date.today()
        time_shift = datetime.combine(today, datetime.now().time()) - datetime.combine(today, game.start_time)
        # посылаем уведомления в интервале [5 минут до начала матча; 5 минут со старта матча]
        if abs(time_shift.total_seconds()) < SYNC_PERIOD:
            await self._notify(game)

    async def send_escaped_message(self, user_id: int, message: types.message, **kwargs):
        """Отправка сообщений с экранированными символами."""
        try:
            await self.send_message(user_id, escape_telegram_char(message), **kwargs)
        except aiogram_exceptions.BotBlocked:
            await clear(user_id)

    async def on_startup(self, dispatcher: Dispatcher):
        """Хук старта приложения."""
        # TODO: need use alembic migrations
        await create_db()
        asyncio.create_task(self.refresh_games())

    def run(self, dispatcher: Dispatcher):
        """Запуск бота."""
        asyncio.run(executor.start_polling(dispatcher, on_startup=self.on_startup))
