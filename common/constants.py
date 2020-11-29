"""Набор констан для бота"""
__author__ = 'Платов М.И.'


class UserMessage:
    """Сообщения для пользователя"""
    START = 'Send me the name of the team you want to broadcast'
    """Приветственное сообщение"""
    NOT_FOUND = "The broadcast hasn't started yet or You've viewed all the available links"
    """Сообщение об отсутствии ссылок"""
    ALL_LINK = 'Found links:'
    """Строковый идентификатор для получения следующей ссылки"""


class SiteInfo:
    """Константы для получение информации с сайта."""
    ADDRESS = 'http://onhockey.tv'
    """Адрес сайта"""
    SCHEDULE = 'schedule_table_eng.php'
    """Расписание матчей"""


class BodyConfig:
    """Конфигурация парсера для парсинга страницы."""
    TABLE = {
        'id': 'gametable'
    }
    """Таблица с расписанием"""
    GAME = {
        'class': 'game'
    }
    """Каждая игра внутри общего расписания"""
