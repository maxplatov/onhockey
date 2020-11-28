"""Запуск бота и реакции на команды"""
__author__ = 'Платов М.И.'

import os

from client.onhockey import Onhockey
from common.constants import START_MSG, NEXT_LINK

onhockey_bot = Onhockey(os.environ['TELEGRAM_TOKEN'])


@onhockey_bot.message_handler(commands=['start', 'go'])
def start_handler(message: dict):
    """Обработка первого сообщения"""
    onhockey_bot.send_message(
        message.chat.id,
        START_MSG
    )


@onhockey_bot.message_handler(content_types=['text'])
def text_handler(message: dict):
    """Обработка всех сообщений"""
    onhockey_bot.send_message(
        message.chat.id,
        onhockey_bot.get_link() if message.text == NEXT_LINK else onhockey_bot.get_link(message.text),
        reply_markup=onhockey_bot.button_markup
    )


onhockey_bot.polling()
