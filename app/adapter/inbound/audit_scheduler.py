
from datetime import datetime, time, timedelta
import logging
from zoneinfo import ZoneInfo
from app.application.usecase.count_day_milk import CountDayMilkInput
from app.config.env_config import env_config
from . import count_day_milk_usecase


def count_day_milk_job():
    try:
        now = datetime.now()
        midnight_tz = datetime.combine(now.date(), time(0, 0))
        midnight = midnight_tz.astimezone(ZoneInfo('UTC'))
        previous_midnight = midnight - timedelta(days=1)
        previous_midnight_tz = previous_midnight.astimezone(
            ZoneInfo(env_config.TZ))
        logging.info(
            f"midnight: {midnight}, previous_midnight: {previous_midnight}, previous_midnight_tz: {previous_midnight_tz}")
        count_day_milk_usecase.execute(CountDayMilkInput(
            previous_day=previous_midnight, previous_day_tz=previous_midnight_tz, now_day=midnight))
    except Exception as e:
        logging.exception(e)
