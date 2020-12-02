"""Класс для работы с данными сайта."""
__author__ = 'Платов М.И.'

import threading
from typing import List, Optional

from telebot import TeleBot

from server.game import Game
from server.site import get_games
from common.constants import SYNC_PERIOD


class Onhockey(TeleBot):
    """Класс Бот - onhockey"""

    games: List[Game] = None

    def __init__(self, token: str, parse_mode: str):
        super().__init__(token, parse_mode=parse_mode)
        self.refresh_games()

    def refresh_games(self):
        """Обновляем данные о текущих играх"""
        threading.Timer(SYNC_PERIOD, self.refresh_games).start()
        self.games = []
        for item in get_games():
            self.games.append(Game(*item))

    def get_sought_game(self, team: str = None) -> Optional[Game]:
        """
        Получить игру по названию команды
        Args:
            team: Название команды

        Returns:
            Игра с ссылками на трансляцию
        """
        if self.games:
            for game in self.games:
                if team in game:
                    return game
        return None
