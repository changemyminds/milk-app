from app.adapter.outbound.line_message_notify import LineMessageNotify
from app.adapter.outbound.line_message_repository import LineMessageRepository
from app.adapter.outbound.transaction_repository import TransactionRepository
from app.domain.service.line_message_parser import LineMessageParser
from app.application.usecase.count_day_milk import CountDayMilkUseCase
from app.application.usecase.delete_line_message import DeleteLineMessageUseCase
from app.application.usecase.parse_line_message import ParseLineMessageUseCase
from app.adapter.outbound.milk_repository import MilkRepository
from app.config.env_config import env_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# database
engine = create_engine(env_config.get_db_connection())
session = sessionmaker(bind=engine)
milk_repository = MilkRepository(session)
line_message_repository = LineMessageRepository(session)
transaction_repository = TransactionRepository(session)

line_message_notify = LineMessageNotify(env_config.LINE_NOTIFY_TOKEN)

parse_line_message_usecase = ParseLineMessageUseCase(
    env_config.PRIVATE_GROUP_ID, transaction_repository, milk_repository, LineMessageParser())

delete_line_message_usecase = DeleteLineMessageUseCase(
    line_message_repository, milk_repository, transaction_repository, line_message_notify)

count_day_milk_usecase = CountDayMilkUseCase(
    milk_repository, line_message_notify)
