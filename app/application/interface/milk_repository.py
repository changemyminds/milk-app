from datetime import datetime
from typing import List
from app.domain.milk_entity import MilkEntity


class MilkRepository:
    def add(self, entity: MilkEntity):
        raise NotImplementedError

    def get(self, entity_id: int) -> MilkEntity:
        raise NotImplementedError
 

    def get_milks_range(self, day_start: datetime, day_end: datetime) -> List[MilkEntity]:
        raise NotImplementedError