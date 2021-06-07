import logging
import requests
from decouple import config
import json


class Telegram():
    def __init__(self):
        self.URL = 'https://api.telegram.org/bot' + config("TELEGRAM_TOKEN")

    def send_message(self, chat_id, message="", image=None):
        data = {
            "chat_id": chat_id,
            "parse_mode": "HTML",
            "text": message,
            "reply_markup": {
                "keyboard": [[{
                    "text": "/fullreport"
                },
                    {
                    "text": "/text"
                },
                    {
                    "text": "/image"
                }]],
                "resize_keyboard": True,
            },
            "disable_notification": True,
        }
        endpoint = "/sendMessage"

        res = requests.get(self.URL + endpoint, json=data)
        logging.info(res.json())

        if image:
            endpoint = '/sendPhoto'
            data['photo'] = image
            res = requests.post(self.URL + endpoint, json=data)

            logging.info(res.json())
            return

    def get_updates(self, offset):
        endpoint = "/getUpdates"
        res = requests.get(self.URL + endpoint,
                           json={
                               'timeout': 200,
                               'offset': offset
                           })

        update = json.loads(res.content.decode('utf-8'))['result']

        return update
