import logging
from typing import Optional
from sqlalchemy.orm import sessionmaker
from app.adapter.outbound.model import LineMessage
from app.application.interface.line_message_port import LineMessagePort
from sqlalchemy import delete, exc, exists, select

from app.domain.line_message_entity import LineMessageEntity


class LineMessageRepository(LineMessagePort):
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    def findByMessageId(self, message_id: str) -> Optional[LineMessageEntity]:
        with self.sessionmaker() as session:
            stmt = select(LineMessage).where(
                LineMessage.message_id == message_id)
            result = session.execute(stmt).scalar_one_or_none()

            if result:
                return LineMessageEntity(
                    id=result.id,
                    message_id=result.message_id,
                    text=result.text,
                    type=result.type,
                    group_id=result.group_id,
                    user_id=result.user_id,
                    timestamp=result.timestamp
                )
            return None

    def existByMessageId(self, message_id: str) -> bool:
        with self.sessionmaker() as session:
            stmt = select(exists().where(LineMessage.message_id == message_id))
            result = session.execute(stmt).scalar()

            return result
