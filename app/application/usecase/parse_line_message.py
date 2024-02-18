from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.application.interface.line_message_port import LineMessagePort
from app.application.interface.milk_port import MilkPort
from app.application.interface.transaction_port import TransactionPort
from app.application.service.line_message_parser import LineMessageParser
from app.domain.line_message_entity import LineMessageEntity
from app.domain.milk_entity import MilkEntity


class ParseLineMessageInput(BaseModel):
    timestamp: int
    message_id: str
    group_id: str
    user_id: str
    text: str
    type: str
    is_redelivery: bool


class ParseLineMessageOutput(BaseModel):
    message: str


class ParseLineMessageUseCase:
    def __init__(self, private_group_id: str, transaction_port: TransactionPort, line_message_port: LineMessagePort, line_message_parser: LineMessageParser):
        self.private_group_id = private_group_id
        self.transaction_port = transaction_port
        self.line_message_port = line_message_port
        self.line_message_parser = line_message_parser

    def execute(self, input: ParseLineMessageInput) -> ParseLineMessageOutput:
        if self.private_group_id != input.group_id:
            raise ValueError("The group id is not correct")

        # check line message redelivery
        if input.is_redelivery:
            exist = self.line_message_port.existByMessageId(input.message_id)
            if exist:
                raise ValueError(f"The message_id has been existed: {input.message_id}")

        time, cc = self.line_message_parser.parse_breast_milk_record(
            input.text)
        timestamp_s = input.timestamp / 1000  # convert to sec
        create_time = datetime.fromtimestamp(timestamp_s)

        line_message_entity = LineMessageEntity.new(
            input.message_id, input.type, input.group_id, input.user_id, input.text, create_time)
        milk_entity = MilkEntity.new(time, cc, create_time)
        self.transaction_port.addLineMessageAndMilkRecord(
            line_message_entity, milk_entity)

        message = self.__create_success_message(milk_entity.time_range, milk_entity.cc)
        return ParseLineMessageOutput(message=message)

    def __create_success_message(self, time: str, cc: int) -> str:
        messages = []
        messages.append(f"時間: {time} 🕐")
        messages.append(f"cc數: {cc} 🍼")
        messages.append(f"狀態: 紀錄成功 🎉")
        return "\n".join(messages)
