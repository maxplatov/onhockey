"""Описание таблицы teams"""
__author__ = 'Платов М.И.'

from . import db


class Teams(db.Model):
    """Таблица всех команд"""
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
