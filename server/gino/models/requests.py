"""Описание таблицы requests"""
__author__ = 'Платов М.И.'

from . import db
from .teams import Teams


class Requests(db.Model):
    """Пользовательские запросы команд"""
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    team_id = db.Column(None, db.ForeignKey(Teams.__tablename__ + '.id'))
