from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.adapter.inbound.line_controller import linebot_bp
from app.adapter.inbound.scheduler import count_day_milk_job
import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=log_format)

# flask run
logging.info("flask run")
app = Flask(__name__)
app.register_blueprint(linebot_bp)

# scheduler run
logging.info("scheduler run")
scheduler = BackgroundScheduler()
scheduler.add_job(count_day_milk_job, 'cron', day='*', hour=1, minute=0, timezone='Asia/Taipei')
scheduler.start()
