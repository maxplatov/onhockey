"""Вспомогательные функции"""
__author__ = 'Платов М.И.'

from transliterate import translit
from telebot import types

from common.constants import NEXT_LINK

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


def get_button_markup():
    """Кнопка для получения следующей ссылки"""
    source_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    source_markup_btn1 = types.KeyboardButton(NEXT_LINK)
    source_markup.add(source_markup_btn1)
