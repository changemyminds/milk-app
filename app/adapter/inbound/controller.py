import logging
from flask import Blueprint, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from application.usecase.parse_line_message import ParseLineMessageInput, ParseLineMessageOutput
from . import parse_line_message_usecase

from typing import List, Optional
from pydantic import BaseModel
from config.env_config import env_config

linebot_bp = Blueprint('linebot_bp', __name__)


class Source(BaseModel):
    type: str
    groupId: Optional[str] = None
    userId: Optional[str] = None


class DeliveryContext(BaseModel):
    isRedelivery: bool


class Message(BaseModel):
    type: str
    id: str
    quoteToken: Optional[str] = None
    text: str


class Event(BaseModel):
    type: str
    message: Message
    webhookEventId: str
    deliveryContext: DeliveryContext
    timestamp: int
    source: Source
    replyToken: str
    mode: str


class WebhookPayload(BaseModel):
    destination: str
    events: List[Event]


@linebot_bp.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        line_bot_api = LineBotApi(env_config.LINE_ACCESS_TOKEN)
        handler = WebhookHandler(env_config.LINE_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        payload = WebhookPayload.model_validate(json_data)

        logging.info(payload)
        type = payload.events[0].message.type
        if type == 'text':
            input = ParseLineMessageInput(
                timestamp=payload.events[0].timestamp,
                groupId=payload.events[0].source.groupId,
                userId=payload.events[0].source.userId,
                text=payload.events[0].message.text
            )
            output: ParseLineMessageOutput = parse_line_message_usecase.execute(
                input)

            line_bot_api.reply_message(
                payload.events[0].replyToken, TextSendMessage(output.message))
    except Exception as e:
        logging.error(e)
    return 'OK'
