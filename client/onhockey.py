"""Класс для работы с данными сайта."""
__author__ = 'Платов М.И.'

from typing import List

from telebot import TeleBot, types

from common.func import get_team_name, get_button_markup
from common.constants import NOT_FOUND
from server.site import get_schedule, get_source_link


def call_count_updater(func):
    """Декоратор для подсчета обращений за следующими ссылками."""
    def decorator(this, *args, **kwargs):
        if args[0] is None:
            this.call_count += 1
        else:
            # могли ввести новую команду, сохраненные данные уже не актуальны
            this.reset()
        return func(this, *args, **kwargs)

    return decorator


class Onhockey(TeleBot):
    """Класс Бот - onhockey"""

    __schedule: List[str] = None
    __button_markup: types = None
    call_count = 0

    def __init__(self, token: str):
        super().__init__(token)

    @property
    def button_markup(self):
        """Кнопка получения следующей ссылки"""
        if self.__button_markup is None:
            self.__button_markup = get_button_markup()
        return self.__button_markup

    def reset(self):
        """Сбрасывает свойства в исходное состояние."""
        self.call_count = 0
        self.__schedule = None

    def schedule_list(self, team: str) -> List[str]:
        """
        Массив ссылок трансляций команды
        Args:
            team: Имя команды, под которую ищем ссылки

        Returns:
            Массив ссылок
        """
        if self.__schedule is None:
            self.__schedule = get_schedule(get_team_name(team))
        return self.__schedule

    @call_count_updater
    def get_link(self, team: str = None) -> str:
        """
        Ссылка на трансляцию.
        Args:
            team: Название команды, если первой обращение.

        Returns:
            Ссылка на трансляцию и сообщение об их отсутствии.
        """
        links_len = len(self.schedule_list(team))
        if links_len and links_len - 1 <= self.call_count:
            return get_source_link(self.schedule_list(team)[self.call_count])
        return NOT_FOUND
