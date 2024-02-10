
from datetime import datetime, timedelta
import logging
from application.usecase.count_day_milk import CountDayMilkInput, CountDayMilkOutput
from . import count_day_milk_usecase


def count_day_milk_job():
    # sub 1 day
    now = datetime.now()
    previous_day = now - timedelta(days=1)
    logging.info(previous_day)
    output: CountDayMilkOutput = count_day_milk_usecase.execute(
        CountDayMilkInput(day=previous_day))
    logging.info(output)
