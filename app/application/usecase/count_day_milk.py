from datetime import datetime
import logging
from pydantic import BaseModel
from application.interface.milk_repository import MilkRepository


class CountDayMilkInput(BaseModel):
    day: datetime


class CountDayMilkOutput(BaseModel):
    message: str


class CountDayMilkUseCase:
    def __init__(self, milk_repository: MilkRepository):
        self.milk_repository = milk_repository

    def execute(self, input: CountDayMilkInput) -> CountDayMilkOutput:
        day_start = datetime.combine(input.day, datetime.min.time())
        day_end = datetime.combine(input.day, datetime.max.time())
        milks = self.milk_repository.get_milks_range(day_start, day_end)
        logging.info(milks)
        total_cc = sum([milk.cc for milk in milks])

        # line notify
        message = f"{input.day} - 總共紀錄了{len(milks)}筆, 總共{total_cc}cc"
        return CountDayMilkOutput(message=message)
