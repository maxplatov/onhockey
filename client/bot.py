"""Запуск бота и реакции на команды"""
__author__ = 'Платов М.И.'

import functools
import logging
import os

from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError

from client.onhockey import Onhockey
from server.gino.sql.operations import get_stats
from server.gino.sql.subscriptions import create_subscribes, get_teams, clear
from common.constants import UserMessage, SubscribesMessage
from common.func import get_button_markup, get_all_games, get_formatted_info, get_formatted_subscribes

logger = logging.getLogger(__name__)

onhockey_bot = Onhockey(os.environ['TELEGRAM_TOKEN'], parse_mode=types.ParseMode.MARKDOWN_V2)
dispatcher = Dispatcher(onhockey_bot)


def error_handler(func):
    @functools.wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except TelegramAPIError as api_error:
            logger.warning(f"Telegram API error: {api_error}")
        except Exception as e:
            logger.exception(f"Error {func.__name__}: {e}")
            try:
                await message.answer(UserMessage.ERROR)
            except Exception as inner:
                logger.error(f"Error while message sending: {inner}")
    return wrapper


@dispatcher.message_handler(commands=['start', 'go'])
@error_handler
async def start_handler(message: types.message):
    """Обработка первого сообщения"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        UserMessage.START
    )


@dispatcher.message_handler(commands=['help'])
@error_handler
async def help_handler(message: types.message):
    """Доступные команды"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        UserMessage.HELP + '\n\n' + UserMessage.START
    )


@dispatcher.message_handler(commands=['stats'])
@error_handler
async def top_handler(message: types.message):
    """Статистика бота"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        await get_stats()
    )


@dispatcher.message_handler(commands=['all'])
@error_handler
async def all_handler(message: types.message):
    """Просмотр доступных трансляций"""
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        get_all_games(onhockey_bot.games) if onhockey_bot.games else UserMessage.NOT_FOUND
    )


@dispatcher.message_handler(commands=['add'])
@error_handler
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
@error_handler
async def subscribe_list_handler(message: types.message):
    """Обработка сообщений о списке подписок"""
    teams = await get_teams(message.from_user.id)
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        get_formatted_subscribes(teams) if teams else SubscribesMessage.EMPTY + '\n\n' + SubscribesMessage.HELP
    )


@dispatcher.message_handler(commands=['clear'])
@error_handler
async def clear_subscribes_handler(message):
    """Очистка всех подписок"""
    await clear(message.from_user.id)
    await onhockey_bot.send_escaped_message(
        message.from_user.id,
        SubscribesMessage.CLEAR
    )


@dispatcher.message_handler()
@error_handler
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
