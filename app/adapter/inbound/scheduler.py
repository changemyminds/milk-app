
from datetime import datetime, timedelta
import logging
from application.usecase.count_day_milk import CountDayMilkInput, CountDayMilkOutput
from . import count_day_milk_usecase


def count_day_milk_job():
    try:
        # sub 1 day
        now = datetime.now()
        previous_day = now - timedelta(days=1)
        logging.info(f"now: {now}, previous_day: {previous_day}")
        count_day_milk_usecase.execute(CountDayMilkInput(day=previous_day))
    except Exception as e:
        logging.error(e)
