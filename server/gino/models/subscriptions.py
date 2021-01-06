"""Описание таблицы subscriptions"""
__author__ = 'Платов М.И.'

from . import db
from .teams import Teams


class Subscriptions(db.Model):
    """Подписки на трансляции команд"""
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    team_id = db.Column(None, db.ForeignKey(Teams.__tablename__ + '.id'))
