"""Набор констан для бота"""
__author__ = 'Платов М.И.'

SYNC_PERIOD = 300.0
"""Время через которое обновляем расписание текущих игр в боте.

~ за 20 минут до начала матча появляются первые трансляции
Чем ближе к началу матча, тем больше трансляций добавляется
Даже после начала игры они появляются
Т.е исходный интервал определяем как [-20 мин; 20 мин]
Сами матчи начинаются либо в HH:00, либо HH:30
В итоге 2 пересекающихся временных диапазона, для покрытия которых достаточно 5минутного обновления расписания
"""

TOP_LIMIT = 5
"""Количество команд в ответе для построения топа"""


class UserMessage:
    """Сообщения для пользователя"""
    START = 'Send me the name of the team you want to see, for example: `Lokomotiv`'
    """Приветственное сообщение"""
    NOT_FOUND = "The broadcast hasn't started yet or there are no available links"
    """Сообщение об отсутствии ссылок"""
    ALL_LINK = 'Found links to '
    """Строковый идентификатор для получения следующей ссылки"""
    TOP_TEAMS = 'Most popular requested teams : '
    """Список самых популярных команд"""
    HELP = 'Command : \n' \
           '\- /all \- view current games \n' \
           '\- /top \- popular requested teams '
    """Как пользоваться ботом"""


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
