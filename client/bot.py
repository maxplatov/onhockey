"""Запуск бота и реакции на команды"""
__author__ = 'Платов М.И.'

import os
import time
import datetime

from telebot import types

from client.onhockey import Onhockey
from common.constants import UserMessage
from common.func import get_button_markup

onhockey_bot = Onhockey(os.environ['TELEGRAM_TOKEN'])


@onhockey_bot.message_handler(commands=['start', 'go'])
def start_handler(message: dict):
    """Обработка первого сообщения"""
    onhockey_bot.send_message(
        message.chat.id,
        UserMessage.START
    )


@onhockey_bot.message_handler(commands=['all'])
def start_handler(message: dict):
    """Просмотр доступных трансляций.Отладочная команда."""
    msg = ''
    if onhockey_bot.games:
        for game in onhockey_bot.games:
            msg += game.info
            msg += '\n'
            msg += str(game.links)
    else:
        msg = 'empty'
    onhockey_bot.send_message(
        message.chat.id,
        msg
    )


@onhockey_bot.message_handler(content_types=['text'])
def text_handler(message: dict):
    """Обработка всех сообщений"""
    links = onhockey_bot.get_links(message.text)
    if links:
        onhockey_bot.send_message(
            message.chat.id,
            UserMessage.ALL_LINK,
            reply_markup=get_button_markup(links)
        )
    else:
        onhockey_bot.send_message(
            message.chat.id,
            UserMessage.NOT_FOUND
        )


onhockey_bot.polling()

while True:
    if datetime.datetime.now().minute % 5 == 0:
        onhockey_bot.refresh_games()
    time.sleep(60)
