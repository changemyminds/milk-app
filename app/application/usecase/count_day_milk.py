from datetime import datetime
import logging
from pydantic import BaseModel
from app.application.interface.message_notify import MessageNotify
from app.application.interface.milk_repository import MilkRepository


class CountDayMilkInput(BaseModel):
    day: datetime


class CountDayMilkOutput(BaseModel):
    message: str


class CountDayMilkUseCase:
    def __init__(self, milk_repository: MilkRepository, message_notify: MessageNotify):
        self.milk_repository = milk_repository
        self.message_notify = message_notify

    def execute(self, input: CountDayMilkInput) -> CountDayMilkOutput:
        day_start = datetime.combine(input.day, datetime.min.time())
        day_end = datetime.combine(input.day, datetime.max.time())
        milks = self.milk_repository.get_milks_range(day_start, day_end)
        logging.info(milks)
        total_cc = sum([milk.cc for milk in milks])

        # line notify
        day_format = input.day.strftime("%Y/%m/%d %H:%M:%S")
        message = f"\n時間: {day_format}\n總筆數: {len(milks)}筆\n總cc數: {total_cc}cc"
        self.message_notify.notify(message)
        return CountDayMilkOutput(message=message)
