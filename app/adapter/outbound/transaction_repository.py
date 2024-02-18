import logging
from sqlalchemy import delete
from app.adapter.outbound.model import LineMessage, Milk
from app.application.interface.transaction_port import TransactionPort
from app.domain.milk_entity import MilkEntity
from app.domain.line_message_entity import LineMessageEntity
from sqlalchemy.orm import sessionmaker


class TransactionRepository(TransactionPort):
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def addLineMessageAndMilkRecord(self, line_message_entity: LineMessageEntity, milk_entity: MilkEntity):
        with self.sessionmaker() as session:
            try:
                line_message = LineMessage(
                    message_id=line_message_entity.message_id,
                    text=line_message_entity.text,
                    type=line_message_entity.type,
                    group_id=line_message_entity.group_id,
                    user_id=line_message_entity.user_id,
                    timestamp=line_message_entity.timestamp,
                )
                session.add(line_message)
                session.flush()

                milk = Milk(
                    time_range=milk_entity.time_range,
                    cc=milk_entity.cc,
                    create_time=milk_entity.create_time,
                    line_message_id=line_message.id
                )
                session.add(milk)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def deleteLineMessageAndMilkRecord(self, line_message_id: int, milk_id: int) -> bool:
        with self.sessionmaker() as session:
            try:
                milk_stmt = delete(Milk).where(Milk.id == milk_id)
                session.execute(milk_stmt)

                line_message_stmt = delete(LineMessage).where(LineMessage.id == line_message_id)
                session.execute(line_message_stmt)

                session.commit()
                return True
            except Exception as e:
                session.rollback()
                logging.exception(e)
                return False
