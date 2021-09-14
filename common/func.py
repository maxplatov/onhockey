"""Вспомогательные функции"""
__author__ = 'Платов М.И.'

import re
from typing import List, Optional
from urllib.parse import urlparse

import tldextract
from transliterate import translit
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from server.sources.game import Game

MONOSPACED_MODE = "`"
"""Символ для моноширинности текста"""

ESCAPING_CHARS = ['_', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

VK_VIDEO = "vk.com/video"


def _get_formatted_team_name(team: str) -> str:
    """Имя команды в моноширинном ввиде, чтобы при клике на текст, он копировался"""
    return MONOSPACED_MODE + team + MONOSPACED_MODE


def escape_telegram_char(text: str) -> str:
    """Экранирование обязательных символов телеграмм.
    https://core.telegram.org/bots/api#markdownv2-style"""
    for char in ESCAPING_CHARS:
        if char in text:
            text = text.replace(char, '\\' + char)
    return text


def get_formatted_subscribes(teams: List[str]) -> str:
    """
    Отформатированный список команд на которые подписан пользователь
    Args:
        teams: массив названий команд

    Returns:
        Отформатированная строка
    """
    msg = ''
    for index, team in enumerate(teams):
        if msg:
            msg += '\n'
        msg += str(index + 1) + '. ' + _get_formatted_team_name(team)
    return msg


def get_team_name(team: str) -> str:
    """
    Обрезает и переводит название команды в анлиглийскую транслитерацию
    Args:
        team: Строка с названием команды

    Returns:
        Имя команды английскими буквами
    """
    team_name = team.strip().title()
    if not team_name.isascii():
        try:
            return translit(team_name, reversed=True)
        except:
            return team_name
    return team_name


def get_all_games(games: List[Game]) -> str:
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
        msg += game.start_time.strftime('%H:%M') + ' (GMT0) ' + get_formatted_info(game)
    return msg


def get_domain(url: str) -> str:
    """Извлекает название домена из ссылки."""
    return tldextract.extract(url).domain.split('-')[0]


def get_button_markup(links: List[str]) -> Optional[InlineKeyboardMarkup]:
    """Кнопка для получения следующей ссылки"""
    if links:
        source_markup = InlineKeyboardMarkup()
        for link in links:
            source_markup.add(InlineKeyboardButton(text=escape_telegram_char(get_domain(link)), url=link))
        return source_markup
    return None


def is_vk_link(url: str):
    """Ссылка на видео вконтакте"""
    return VK_VIDEO + "_ext.php" in url


def get_video_from_vk(url: str):
    """Генерация прямой ссылки на видео из ссылки для шэринга"""
    ids = list(map(int, re.findall(r'\d+', url)))
    if ids and len(ids) >= 2:
        return "https://" + VK_VIDEO + f"-{ids[0]}_{ids[1]}"
    return None


def get_valid_link(url: str):
    """Возвращаем url если он корректный"""
    if url:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc and parsed_url.path:
            return parsed_url.geturl()
    return None


def get_formatted_info(game: Game) -> str:
    """Отформатированная для отображения в сообщении строчка играющих команд"""
    return _get_formatted_team_name(game.home) + ' - ' + _get_formatted_team_name(game.guest)
