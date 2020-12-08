"""Описание Базы данных"""
__author__ = 'Платов М.И.'

import os

from server.gino.models import db


async def create_db():
    """Развертывание таблиц и поднятие коннекта к бд"""
    await db.set_bind(os.environ['DATABASE_URL'])
    await db.gino.create_all()
