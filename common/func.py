"""Вспомогательные функции"""
__author__ = 'Платов М.И.'

import re
from typing import List
from urllib.parse import urlparse

from transliterate import translit
from telebot import types

MONOSPACED_MODE = "`"
"""Символ для моноширинности текста"""


def _get_formatted_team_name(team: str) -> str:
    """Имя команды в моноширинном ввиде, чтобы при клике на текст, он копировался"""
    return MONOSPACED_MODE + team + MONOSPACED_MODE


def formatted_top(teams: List[str]) -> str:
    """
    Отформатированный список команд для топа
    Args:
        teams: массив названий команд

    Returns:
        Отформатированную строку для топа
    """
    msg = ''
    for index, team in enumerate(teams):
        if msg:
            msg += '\n'
        msg += str(index + 1) + '\. ' + _get_formatted_team_name(team)
    return msg


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


def get_all_games(games) -> str:
    """
    Все игры, которые транслируются
    Args:
        games: Массив игр
    Returns:
        Team 1 - Team 2
        Team 3 - Team 4
    """
    msg = ''
    for game in games:
        if msg:
            msg += '\n'
        msg += _get_formatted_team_name(game.home) + ' - ' + _get_formatted_team_name(game.guest)
    return msg


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
    info = re.search(r'([A-Za-z].*-.*)', game)
    return info.group(1) if info else None


def get_valid_link(url: str):
    """Возвращаем url если он корректный"""
    if url:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc and parsed_url.path:
            return parsed_url.geturl()
    return None
