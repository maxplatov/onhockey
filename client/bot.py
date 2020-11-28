"""Бот"""
__author__ = 'Платов М.И.'

import os

import telebot


START_MSG = 'Пришли мне имя команды, трансляцию которой ты хочешь получить'


def _create_telebot(token: str):
    """"""
    return telebot.TeleBot(token)


bot = _create_telebot(os.environ['TELEGRAM_TOKEN'])


@bot.message_handler(commands=['start', 'go'])
def start_handler(message: dict):
    """Обработка первого сообщения"""
    bot.send_message(message.chat.id, START_MSG)


@telebot.message_handler(content_types=['text'])
def text_handler(message: dict):
    """Обработка всех сообщений"""
    bot.send_message(message.chat.id, message.text)


bot.polling()
