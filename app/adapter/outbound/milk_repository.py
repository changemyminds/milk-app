from datetime import datetime
import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from app.adapter.outbound.model import Milk
from app.application.interface.milk_port import MilkPort
from app.domain.milk_entity import MilkEntity


class MilkRepository(MilkPort):
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def add(self, entity: MilkEntity):
        with self.sessionmaker() as session:
            milk = Milk(time_range=entity.time_range, cc=entity.cc,
                        create_time=entity.create_time)
            session.add(milk)
            session.commit()

    def get_milks_range(self, day_start: datetime, day_end: datetime) -> List[MilkEntity]:
        logging.info(
            f"day_start: {day_start}, day_end: {day_end}")
        with self.sessionmaker() as session:
            milks = session.query(Milk).\
                filter(Milk.create_time >= day_start).\
                filter(Milk.create_time < day_end).all()

            logging.info(milks)

            # convert milks to MilkEntity
            entities = [MilkEntity(id=milk.id, time_range=milk.time_range,
                                   cc=milk.cc, create_time=milk.create_time) for milk in milks]
            return entities

    def findByLineMessageId(self, line_message_id: str) -> Optional[MilkEntity]:
        with self.sessionmaker() as session:    
            stmt = select(Milk).where(Milk.line_message_id == line_message_id)
            result = session.execute(stmt).scalar_one_or_none()

            if result:
                return MilkEntity(
                    id=result.id,
                    time_range=result.time_range,
                    cc=result.cc,
                    create_time=result.create_time
                )
            return None            