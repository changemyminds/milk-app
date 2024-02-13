from datetime import datetime
import logging
from zoneinfo import ZoneInfo
from pydantic import BaseModel
from app.application.interface.message_notify import MessageNotify
from app.application.interface.milk_repository import MilkRepository


class CountDayMilkInput(BaseModel):
    previous_day: datetime
    previous_day_tz: datetime
    now_day: datetime


class CountDayMilkOutput(BaseModel):
    message: str


class CountDayMilkUseCase:
    def __init__(self, milk_repository: MilkRepository, message_notify: MessageNotify):
        self.milk_repository = milk_repository
        self.message_notify = message_notify

    def execute(self, input: CountDayMilkInput) -> CountDayMilkOutput:         
        milks = self.milk_repository.get_milks_range(input.previous_day, input.now_day)
        total_cc = sum([milk.cc for milk in milks])

        # line notify
        date_format = input.previous_day_tz.strftime("%Y-%m-%d")

        messages = []
        messages.append(f"紀錄時間: {date_format} 🕐")
        count = len(milks)
        if count > 0:
            messages.append(f"詳細資訊如下:")
            for milk in milks:
                messages.append(f"{milk.time_range} - {milk.cc}cc")
        messages.append(f"總筆數: {count} ✏️")
        messages.append(f"總cc數: {total_cc} 🍼")
        message = '\n' + '\n'.join(messages)
        self.message_notify.notify(message)

        return CountDayMilkOutput(message=message)
