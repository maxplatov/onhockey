"""Игра с сайта onhockey"""
__author__ = 'Платов М.И.'

import logging
from datetime import time
from typing import List

import asyncio

from server.sources.game import Game
from server.sources.onhockey.extractor import get_teams, get_source_link

log = logging.getLogger(__name__)


class OnHockeyGame(Game):
    """Игра с сайта"""
    def __init__(self, info: str, start_time: time, channels: List[str]):
        self.channels = channels
        home, guest = get_teams(info)
        super().__init__(home, guest, start_time)

    async def get_links(self):
        """Добавляет ссылку на прямую трансляцию из канала"""
        futures = [get_source_link(channel) for channel in self.channels]
        for res in await asyncio.gather(*futures, return_exceptions=True):
            if isinstance(res, Exception):
                log.info(res)
            elif res:
                self.links.append(res)
