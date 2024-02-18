

import logging
from pydantic import BaseModel

from app.application.interface.line_message_port import LineMessagePort
from app.application.interface.message_notify import MessageNotify
from app.application.interface.milk_port import MilkPort
from app.application.interface.transaction_port import TransactionPort


class DeleteLineMessageInput(BaseModel):
    message_id: str


class DeleteLineMessageOutput(BaseModel):
    pass


class DeleteLineMessageUseCase:
    def __init__(self, line_message_port: LineMessagePort, milk_port: MilkPort, transaction_port: TransactionPort, message_notify: MessageNotify) -> None:
        self.line_message_port = line_message_port
        self.milk_port = milk_port
        self.transaction_port = transaction_port
        self.message_notify = message_notify

    def execute(self, input: DeleteLineMessageInput) -> DeleteLineMessageOutput:
        empty_output = DeleteLineMessageOutput()
        line_message_entity = self.line_message_port.findByMessageId(
            input.message_id)
        if not line_message_entity:
            logging.warn(f"can't find the message_id: {input.message_id}")
            return empty_output

        milk_entity = self.milk_port.findByLineMessageId(
            line_message_entity.id)
        if not milk_entity:
            logging.warn(
                f"can't find the line_message_id: {line_message_entity.id}")
            return empty_output

        result = self.transaction_port.deleteLineMessageAndMilkRecord(
            line_message_id=line_message_entity.id, milk_id=milk_entity.id)
        if not result:
            logging.warn(
                f"delete line_message and milk failed: {line_message_entity.id}, {milk_entity.id}")
            return empty_output

        message = self.__delete_success_message(line_message_entity.text)
        self.message_notify.notify(message=message)

        return empty_output

    def __delete_success_message(self, text: str) -> str:
        messages = []
        messages.append(f"刪除訊息: {text} 💬")
        messages.append("狀態: 刪除成功 🎉")
        return '\n' + "\n".join(messages)
