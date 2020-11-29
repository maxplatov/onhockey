"""Вспомогательные функции"""
__author__ = 'Платов М.И.'

import re
from typing import List

from transliterate import translit
from telebot import types

ENGLISH_TEXT = 'en'


def get_team_name(team: str) -> str:
    """
    Обрезает и переводит название команды в анлиглийскую транслитерацию
    Args:
        team: Строка с названием команды

    Returns:
        Имя команды английскими буквами
    """
    first_name = team.split(' ')[0].lower()
    if not first_name.isascii():
        try:
            return translit(first_name, reversed=True)
        except:
            return first_name
    return first_name


def get_button_markup(links: List[str]) -> types:
    """Кнопка для получения следующей ссылки"""
    if links:
        source_markup = types.InlineKeyboardMarkup()
        for link in links:
            source_markup.add(types.InlineKeyboardButton(text=link, url=link))
        return source_markup
    return None


def get_teams_info(game: str) -> str:
    """
    Возвращает строку с названием играющих команж
    Args:
        game: Метаданные игры

    Returns:
        Team 1 - Team 2
    """
    return re.search(r'\n(.*-.*)\n', game).group(1)
