from sqlalchemy import Column, Integer, String

from app.orm.base import Base


class Team(Base):
    """All teams table"""
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
