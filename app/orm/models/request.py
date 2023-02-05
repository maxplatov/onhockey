from sqlalchemy import Column, Integer, ForeignKey

from app.orm.base import Base
from app.orm.models import Team


class Request(Base):
    """Users requests"""
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    team_id = Column(None, ForeignKey(Team.__tablename__ + '.id'))
