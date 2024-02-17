from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.adapter.inbound.line_controller import linebot_bp
from app.adapter.inbound.audit_scheduler import count_day_milk_job
from yoyo import read_migrations, get_backend
from app.config.env_config import env_config
import logging

log_format = '%(asctime)s.%(msecs)03dZ %(levelname)s [%(name)s] <%(thread)d> - %(filename)s:%(funcName)s():(%(lineno)d) - %(message)s'
log_time_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=log_format,
                    datefmt=log_time_format)


logging.info("database migration")
backend = get_backend(env_config.get_db_connection())
migrations = read_migrations(env_config.MIGRATIONS)
backend.apply_migrations(backend.to_apply(migrations))

logging.info("flask run")
app = Flask(__name__)
app.register_blueprint(linebot_bp)

logging.info("scheduler run")
scheduler = BackgroundScheduler()
scheduler.add_job(count_day_milk_job, 'cron', day='*', hour=0,
                  minute=1, timezone=env_config.TIMEZONE)
scheduler.start()
