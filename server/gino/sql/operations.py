"""Взаимодействие с базой данных"""
__author__ = 'Платов М.И.'

from server.gino.models import db
from server.gino.models.requests import Requests
from server.gino.models.subscriptions import Subscriptions


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
    data = await requests.union_all(subscriptions).gino.all()
    return '\n'.join([record[0] + '. ' + record[1] for record in data])
