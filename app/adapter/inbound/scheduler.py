
from datetime import datetime, time, timedelta
import logging
from zoneinfo import ZoneInfo
from app.application.usecase.count_day_milk import CountDayMilkInput, CountDayMilkOutput
from . import count_day_milk_usecase


def count_day_milk_job():
    try:
        # sub 1 day
        now_asia = datetime.now(ZoneInfo('Asia/Taipei'))
        midnight_asia = datetime.combine(now_asia.date(), time(0, 0), tzinfo=ZoneInfo('Asia/Taipei'))
        now_day = midnight_asia.astimezone(ZoneInfo('UTC'))
        previous_day = now_day - timedelta(days=1)
        logging.info(f"now_day: {now_day}, previous_day: {previous_day}")
        count_day_milk_usecase.execute(CountDayMilkInput(previous_day=previous_day, now_day=now_day))
    except Exception as e:
        logging.error(e)
