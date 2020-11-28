"""Бот"""
__author__ = 'Платов М.И.'

import telebot

from common.constants import GENERAL_TOKEN


START_MSG = 'Пришли мне имя команды, трансляцию которой ты хочешь получить'


def _create_telebot(token: str):
    """"""
    return telebot.TeleBot(token)


telebot = _create_telebot(GENERAL_TOKEN)


@telebot.message_handler(commands=['start', 'go'])
def start_handler(message: dict):
    """Обработка первого сообщения"""
    telebot.send_message(message.chat.id, START_MSG)


@telebot.message_handler(content_types=['text'])
def text_handler(message: dict):
    """Обработка всех сообщений"""
    telebot.send_message(message.chat.id, message.text)


telebot.polling()
