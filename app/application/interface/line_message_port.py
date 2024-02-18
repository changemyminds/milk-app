from typing import Optional
from app.domain.line_message_entity import LineMessageEntity


class LineMessagePort:
    def findByMessageId(self, message_id: str) -> Optional[LineMessageEntity]:
        raise NotImplementedError

    def existByMessageId(self, message_id: str) -> bool:
        raise NotImplementedError
