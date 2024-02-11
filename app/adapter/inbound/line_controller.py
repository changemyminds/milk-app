import logging
from flask import Blueprint, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from app.application.usecase.parse_line_message import ParseLineMessageInput, ParseLineMessageOutput
from app.config.env_config import env_config
from . import parse_line_message_usecase
from typing import List, Optional
from pydantic import BaseModel
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

linebot_bp = Blueprint('linebot_bp', __name__)
line_bot_api = LineBotApi(env_config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(env_config.LINE_SECRET)


class Source(BaseModel):
    type: str
    group_id: Optional[str] = None
    user_id: Optional[str] = None


class DeliveryContext(BaseModel):
    is_redelivery: bool


class Message(BaseModel):
    type: str
    id: str
    quote_token: Optional[str] = None
    text: str


class LineMessageEvent(BaseModel):
    type: str
    message: Message
    webhook_event_id: str
    delivery_context: DeliveryContext
    timestamp: int
    source: Source
    reply_token: str
    mode: str


@linebot_bp.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    logging.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        logging.error(e)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: LineMessageEvent):
    try:
        input = ParseLineMessageInput(
            timestamp=event.timestamp,
            groupId=event.source.group_id,
            userId=event.source.user_id,
            text=event.message.text
        )
        output: ParseLineMessageOutput = parse_line_message_usecase.execute(
            input)

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(output.message))
    except Exception as e:
        logging.warn(e)