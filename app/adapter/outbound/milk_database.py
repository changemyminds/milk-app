import datetime
from datetime import datetime
import logging
from typing import List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from app.application.interface.milk_repository import MilkRepository
from app.domain.milk_entity import MilkEntity
from . import Base

class Milk(Base):
    __tablename__ = 'milks'

    id = Column(Integer, primary_key=True)
    time_range = Column(String)
    cc = Column(Integer)
    create_time = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Milk(time_range='{self.time_range}', cc='{self.cc}', create_time='{self.create_time}')>"


class MilkDatabase(MilkRepository):
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def add(self, entity: MilkEntity):
        session = self.sessionmaker()
        with self.sessionmaker() as session:
            milk = Milk(time_range=entity.time_range, cc=entity.cc,
                    create_time=entity.create_time)
            session.add(milk)
            session.commit()
            session.close()

    def get_milks_range(self, day_start: datetime, day_end: datetime) -> List[MilkEntity]:
        with self.sessionmaker() as session:
            session = self.sessionmaker()
            milks = session.query(Milk).\
                filter(Milk.create_time >= day_start).\
                filter(Milk.create_time <= day_end).all()
            
            logging.info(milks)

            # convert milks to MilkEntity
            entities = [MilkEntity(id=milk.id, time_range=milk.time_range,
                               cc=milk.cc, create_time=milk.create_time) for milk in milks]
            return entities
