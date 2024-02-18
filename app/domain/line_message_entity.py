from datetime import datetime


class LineMessageEntity:
    def __init__(self, id: int, message_id: str, text: str, type: str, group_id: str, user_id: str, timestamp: datetime):
        self.id = id
        self.message_id = message_id
        self.text = text
        self.type = type
        self.group_id = group_id
        self.user_id = user_id
        self.timestamp = timestamp

    @classmethod
    def new(cls, message_id: str, type: str, group_id: str, user_id: str, text: str, timestamp: datetime):
        return cls(
            id=None,
            message_id=message_id,
            text=text,
            type=type,
            group_id=group_id,
            user_id=user_id,
            timestamp=timestamp
        )
