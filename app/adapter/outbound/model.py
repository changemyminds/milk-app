from datetime import datetime
from . import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, DateTime

class LineMessage(Base):
    __tablename__ = 'line_messages'

    id = Column(Integer, primary_key=True)
    message_id = Column(String(64), nullable=False)
    text = Column(String(256))
    type = Column(String(32), nullable=False)
    group_id = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)

    def __repr__(self):
        return f"<LineMessage(id={self.id}, message_id='{self.message_id}', text='{self.text}', type='{self.type}', group_id='{self.group_id}', user_id='{self.user_id}', timestamp='{self.timestamp}')>"


class Milk(Base):
    __tablename__ = 'milks'

    id = Column(Integer, primary_key=True)
    time_range = Column(String)
    cc = Column(Integer)
    create_time = Column(DateTime, default=datetime.utcnow)
    line_message_id = Column(Integer, ForeignKey('line_messages.id'))

    def __repr__(self):
        return f"<Milk(id={self.id}, time_range='{self.time_range}', cc='{self.cc}', create_time='{self.create_time}', line_message_id='{self.line_message_id}')>"
