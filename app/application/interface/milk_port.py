from datetime import datetime
from typing import List, Optional
from app.domain.milk_entity import MilkEntity


class MilkPort:
    def add(self, entity: MilkEntity):
        raise NotImplementedError

    def get_milks_range(self, day_start: datetime, day_end: datetime) -> List[MilkEntity]:
        raise NotImplementedError
 
    def findByLineMessageId(self, line_message_id: str) -> Optional[MilkEntity]:
        raise NotImplementedError