from app.domain.milk_entity import MilkEntity
from app.domain.line_message_entity import LineMessageEntity


class TransactionPort:
    def addLineMessageAndMilkRecord(self, line_message_entity: LineMessageEntity, milk_entity: MilkEntity):
        raise NotImplementedError

    def deleteLineMessageAndMilkRecord(self, line_message_id: int, milk_id: int) -> bool:
        raise NotImplementedError