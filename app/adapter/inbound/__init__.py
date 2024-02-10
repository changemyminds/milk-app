import logging
from application.service.line_message_parser import LineMessageParser
from application.usecase.count_day_milk import CountDayMilkUseCase
from application.usecase.parse_line_message import ParseLineMessageUseCase
from adapter.outbound.milk_database import MilkDatabase
from config.env_config import env_config
from sqlalchemy.orm import sessionmaker
from adapter.outbound import engine, Base

import socket

print(socket.gethostbyname('localhost'))

session = sessionmaker(bind=engine)
milk_database = MilkDatabase(session)
Base.metadata.create_all(engine)
 
parse_line_message_usecase = ParseLineMessageUseCase(
    env_config.PRIVATE_GROUP_ID, milk_database, LineMessageParser())

count_day_milk_usecase = CountDayMilkUseCase(milk_database)
