"""Запуск бота и реакции на команды"""
__author__ = 'Платов М.И.'

import os

from aiogram import types
from aiogram.dispatcher import Dispatcher

from client.onhockey import Onhockey
from server.gino.sql.operations import get_stats
from server.gino.sql.subscriptions import create_subscribes, get_teams, clear
from common.constants import UserMessage, SubscribesMessage
from common.func import get_button_markup, get_all_games, get_formatted_info, get_formatted_subscribes

onhockey_bot = Onhockey(os.environ['TELEGRAM_TOKEN'], parse_mode=types.ParseMode.MARKDOWN_V2)
dispatcher = Dispatcher(onhockey_bot)


@dispatcher.message_handler(commands=['start', 'go'])
async def start_handler(message: types.message):
    """Обработка первого сообщения"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        UserMessage.START
    )


@dispatcher.message_handler(commands=['help'])
async def help_handler(message: types.message):
    """Доступные команды"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        UserMessage.HELP + '\n\n' + UserMessage.START
    )


@dispatcher.message_handler(commands=['stats'])
async def top_handler(message: types.message):
    """Статистика бота"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        await get_stats()
    )


@dispatcher.message_handler(commands=['all'])
async def all_handler(message: types.message):
    """Просмотр доступных трансляций"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        get_all_games(onhockey_bot.games) if onhockey_bot.games else UserMessage.NOT_FOUND
    )


@dispatcher.message_handler(commands=['add'])
async def add_handler(message: types.message):
    """Обработка сообщений о подписке на команду."""
    msg = message.text.replace('/add', '')
    if not msg:
        await onhockey_bot.send_escaped_message(
            message.from_user.id,
            SubscribesMessage.HELP
        )
    else:
        result = await create_subscribes(msg, message.from_user.id)
        await onhockey_bot.send_escaped_message(
            message.from_user.id,
            SubscribesMessage.SUCCESS if result else SubscribesMessage.ERROR
        )


@dispatcher.message_handler(commands=['list'])
async def subscribe_list_handler(message: types.message):
    """Обработка сообщений о списке подписок"""
    teams = await get_teams(message.from_user.id)
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        get_formatted_subscribes(teams) if teams else SubscribesMessage.EMPTY + '\n\n' + SubscribesMessage.HELP
    )


@dispatcher.message_handler(commands=['clear'])
async def clear_subscribes_handler(message):
    """Очистка всех подписок"""
    await clear(message.from_user.id)
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        SubscribesMessage.CLEAR
    )


@dispatcher.message_handler()
async def text_handler(message: types.message):
    """Обработка всех сообщений"""
    current_game = await onhockey_bot.get_sought_game(message.text, message.from_user.id)
    markup = get_button_markup(current_game.links) if current_game else None
    if markup:
        await onhockey_bot.send_escaped_message(
            message.from_user.id,
            UserMessage.ALL_LINK + get_formatted_info(current_game),
            reply_markup=markup
        )
    else:
        await onhockey_bot.send_escaped_message(
            message.from_user.id,
            UserMessage.NOT_FOUND
        )


def run():
    """Запуск бота и поднятие коннектов к базе."""
    onhockey_bot.run(dispatcher)
