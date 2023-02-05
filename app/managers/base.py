from loguru import logger

from sqlalchemy import select, desc, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.orm.engine import Base


class BaseAdapter:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def exec(self, stmt):
        try:
            return await self.db_session.execute(stmt)
        except SQLAlchemyError as e:
            logger.exception(e)

    async def get_all(self, stmt):
        result = await self.exec(stmt) or []
        return result and result.scalars().all()

    async def insert(self, model):
        self.db_session.add(model)
        try:
            await self.db_session.flush()
        except SQLAlchemyError as e:
            logger.error(e)
        await self.db_session.refresh(model)
        return model


class BaseManager(BaseAdapter):
    def __init__(self, entity: Base, db_session: Session):
        self.entity = entity
        super().__init__(db_session)

    @property
    def select(self):
        return select(self.entity).order_by(desc(self.entity.id))

    async def get_one(self, pk: int):
        result = await self.exec(
            self.select.where(self.entity.id == pk)
        )
        return result and result.scalars().one()
