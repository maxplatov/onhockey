"""Класс для работы с данными сайта."""
__author__ = 'Платов М.И.'

from typing import List

from telebot import TeleBot

from server.game import Game
from server.site import get_games


class Onhockey(TeleBot):
    """Класс Бот - onhockey"""

    games: List[Game] = None

    def __init__(self, token: str):
        super().__init__(token)
        self.refresh_games()

    def refresh_games(self):
        """Обновляем данные о текущих играх"""
        self.games = []
        for item in get_games():
            self.games.append(Game(*item))

    def get_links(self, team: str = None) -> List[str]:
        """
        Ссылки на трансляции.
        Args:
            team: Название команды

        Returns:
            Ссылки на доступные трансляции
        """
        if self.games:
            for game in self.games:
                if team in game:
                    return game.links
        return []
