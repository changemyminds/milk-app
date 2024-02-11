from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.application.interface.milk_repository import MilkRepository
from app.application.service.line_message_parser import LineMessageParser
from app.domain.milk_entity import MilkEntity


class ParseLineMessageInput(BaseModel):
    timestamp: int
    groupId: Optional[str] = None
    userId: Optional[str] = None
    text: str


class ParseLineMessageOutput(BaseModel):
    message: str


class ParseLineMessageUseCase:
    def __init__(self, private_group_id: str, milk_repository: MilkRepository, line_message_parser: LineMessageParser):
        self.private_group_id = private_group_id
        self.milk_repository = milk_repository
        self.line_message_parser = line_message_parser

    def execute(self, input: ParseLineMessageInput) -> ParseLineMessageOutput:
        if self.private_group_id != input.groupId:
            raise ValueError("The group id is not correct")

        time, cc = self.line_message_parser.parse_breast_milk_record(
            input.text)
        timestamp_s = input.timestamp / 1000  # convert to sec
        create_time = datetime.fromtimestamp(timestamp_s)

        # add milk record
        self.milk_repository.add(entity=MilkEntity(
            id=0, time_range=time, cc=cc, create_time=create_time))
 
        message = self.__create_success_message(time, cc)

        return ParseLineMessageOutput(message=message)

    def __create_success_message(self, time: str, cc: int) -> str:
        messages = []
        messages.append(f"時間: {time} 🕐")
        messages.append(f"cc數: {cc} 🍼")
        messages.append(f"狀態: 紀錄成功 🎉")
        return "\n".join(messages)
