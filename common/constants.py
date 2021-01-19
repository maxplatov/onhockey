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


class UserMessage:
    """Сообщения для пользователя"""
    START = 'Send me the name of the team you want to see, for example: `Lokomotiv` \n' \
            'or view schedule - /all'
    """Приветственное сообщение"""
    NOT_FOUND = "The broadcast hasn't started yet or there are no available links"
    """Сообщение об отсутствии ссылок"""
    ALL_LINK = 'Found links to '
    """Строковый идентификатор для получения следующей ссылки"""
    START_GAME = 'Soon will start '
    """Сообщение о начале игры у команды, на которую подписан"""
    HELP = 'Command : \n' \
           '- /all - view current games \n' \
           '- /add - subscribe to team games \n' \
           '- /list - list of subscriptions \n' \
           '- /clear - clear ALL subscriptions'
    """Как пользоваться ботом"""


class SubscribesMessage:
    """Сообщения для раздела подписок"""
    HELP = "To subscribe to your favorite team's matches send: \n " \
           "- /add Team name \n" \
           "For example: /add `Lokomotiv`"
    """Подписка на команду"""
    SUCCESS = 'Success! Command list updated.'
    """Успешная подписка"""
    ERROR = 'Team not found, try again.'
    """Неудавшаяся подписка"""
    CLEAR = 'Subscriptions removed!'
    """Очистка подписок"""
    EMPTY = 'Subscriptions list is empty.'
    """Нет подписок"""
