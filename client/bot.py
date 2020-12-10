"""Запуск бота и реакции на команды"""
__author__ = 'Платов М.И.'

import os

from aiogram import types
from aiogram.dispatcher import Dispatcher

from client.onhockey import Onhockey
from server.gino.operations import top_request_team
from common.constants import UserMessage
from common.func import get_button_markup, get_all_games, formatted_top

onhockey_bot = Onhockey(os.environ['TELEGRAM_TOKEN'], parse_mode=types.ParseMode.MARKDOWN_V2)
dispatcher = Dispatcher(onhockey_bot)


@dispatcher.message_handler(commands=['start', 'go'])
async def start_handler(message: types.message):
    """Обработка первого сообщения"""
    await onhockey_bot.send_message(
        message.from_user.id,
        UserMessage.START
    )


@dispatcher.message_handler(commands=['help'])
async def help_handler(message: types.message):
    """Доступные команды"""
    await onhockey_bot.send_message(
        message.from_user.id,
        UserMessage.HELP + '\n' + UserMessage.START
    )


@dispatcher.message_handler(commands=['top'])
async def top_handler(message: types.message):
    """Доступные команды"""
    await onhockey_bot.send_message(
        message.from_user.id,
        UserMessage.TOP_TEAMS + '\n' + formatted_top(await top_request_team())
    )


@dispatcher.message_handler(commands=['all'])
async def all_handler(message: types.message):
    """Просмотр доступных трансляций"""
    await onhockey_bot.send_message(
        message.from_user.id,
        get_all_games(onhockey_bot.games) if onhockey_bot.games else UserMessage.NOT_FOUND
    )


@dispatcher.message_handler()
async def text_handler(message: types.message):
    """Обработка всех сообщений"""
    current_game = await onhockey_bot.get_sought_game(message.text, message.from_user.id)
    markup = get_button_markup(current_game.links) if current_game else None
    if markup:
        await onhockey_bot.send_message(
            message.from_user.id,
            UserMessage.ALL_LINK + current_game.info.replace('-', '\-'),
            reply_markup=markup
        )
    else:
        await onhockey_bot.send_message(
            message.from_user.id,
            UserMessage.NOT_FOUND
        )


def run():
    """Запуск бота и поднятие коннектов к базе."""
    onhockey_bot.run(dispatcher)
