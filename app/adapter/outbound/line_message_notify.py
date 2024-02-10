

import logging
import requests
from application.interface.message_notify import MessageNotify


class LineMessageNotify(MessageNotify):
    def __init__(self, line_notify_token: str):
        self.line_notify_token = line_notify_token

    def notify(self, message: str):
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'message': message}

        try:
            response = requests.post(
                line_notify_api, headers=headers, data=data)
            if response.status_code == 200:
                logging.info("Message sent successfully.")
            else:
                # Log error response for debugging
                logging.error(
                    f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
                raise Exception("Failed to send message via Line Notify")
        except requests.exceptions.RequestException as e:
            logging.error(
                f"An error occurred while sending message via Line Notify: {e}")
            raise Exception(
                "An error occurred while sending message via Line Notify")
