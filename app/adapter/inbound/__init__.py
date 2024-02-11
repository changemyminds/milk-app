from app.adapter.outbound.line_message_notify import LineMessageNotify
from app.application.service.line_message_parser import LineMessageParser
from app.application.usecase.count_day_milk import CountDayMilkUseCase
from app.application.usecase.parse_line_message import ParseLineMessageUseCase
from app.adapter.outbound.milk_database import MilkDatabase
from app.config.env_config import env_config
from app.adapter.outbound import engine, Base
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=engine)
milk_database = MilkDatabase(session)
Base.metadata.create_all(engine)

line_message_notify = LineMessageNotify(env_config.LINE_NOTIFY_TOKEN)

parse_line_message_usecase = ParseLineMessageUseCase(
    env_config.PRIVATE_GROUP_ID, milk_database, LineMessageParser())

count_day_milk_usecase = CountDayMilkUseCase(
    milk_database, line_message_notify)
