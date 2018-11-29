from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime

class Draft(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    team = Column(String(50))

    def __init__(self, team=None):
        self.team = name

        def __repr__(self):
            return '<Team Name %r>' % (self.team)


    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    player = Column(String(50))
    team = Column(String(50))

    def __init__(self, player=None, team=None):
        self.player = player
        self.team = team

        def __repr__(self):
            return '<Player %r' % (self.player)
