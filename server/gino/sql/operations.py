"""Взаимодействие с базой данных"""
__author__ = 'Платов М.И.'

from server.gino.models import db
from server.gino.models.requests import Requests
from server.gino.models.subscriptions import Subscriptions

MIN_REQUEST_COUNT_FOR_REGULAR_USER = 5
"""Минимальное количество запросов для того чтобы считать пользователя постоянным."""


async def get_stats() -> str:
    """Статистика по использованию бота."""
    requests = db.select([
        db.func.concat(
            db.func.text('Requests - '),
            db.func.count(Requests.id)
        ),
        db.func.concat(
            db.func.text('Unique users - '),
            db.func.count(db.func.distinct(Requests.user_id))
        )
    ]).select_from(
        Requests
    )
    requests_regular = db.select([
        db.func.concat(
            db.func.text('Regular users - '),
            db.func.count(db.text('*')),
            db.func.text(' (more than ' + str(MIN_REQUEST_COUNT_FOR_REGULAR_USER) + ' requests)')
        ),
        db.func.text('')
    ]).select_from(
        db.select([
            Requests.user_id
        ]).select_from(
            Requests
        ).group_by(
            Requests.user_id
        ).having(
            db.func.count(db.func.text('*')) > MIN_REQUEST_COUNT_FOR_REGULAR_USER
        ).alias('tmp')
    )
    subscriptions = db.select([
        db.func.concat(
            db.func.text('Subscriptions - '),
            db.func.count(Subscriptions.id),
        ),
        db.func.concat(
            db.func.text('Unique users - '),
            db.func.count(db.func.distinct(Subscriptions.user_id)),
        )
    ]).select_from(
        Subscriptions
    )
    data = await subscriptions.union_all(requests.union_all(requests_regular)).gino.all()
    return '\n'.join([record[0] + '. ' + record[1] for record in data])
