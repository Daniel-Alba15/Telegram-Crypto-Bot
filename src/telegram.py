import logging
import requests
from decouple import config
import json
from my_binance import Binance
from image import Image
from imgur import Imgur


class Telegram():
    def __init__(self):
        self.URL = 'https://api.telegram.org/bot' + config("TELEGRAM_TOKEN")

    def _send_message(self, message, chat_id, image=None):
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
        print(res.json())
        logging.info(res.json())

        if image:
            endpoint = '/sendPhoto'
            data['photo'] = image
            res = requests.post(self.URL + endpoint, json=data)
            print(res.json())


            logging.info(res.json())
            return

    def _get_updates(self, offset):
        endpoint = "/getUpdates"
        res = requests.get(self.URL + endpoint,
                           json={
                               'timeout': 200,
                               'offset': offset
                           })

        update = json.loads(res.content.decode('utf-8'))['result']

        return update

    def main(self):
        offset = 0
        binance_info = Binance()
        image_info = Image()

        while (True):
            updates = self._get_updates(offset)
            logging.info(updates)

            print(offset)
            print(updates)

            if updates:
                if offset == 0:
                    offset = updates[0]['update_id']

                print(updates)
                user_id = updates[0]['message']['from']['id']
                chat_id = updates[0]['message']['chat']['id']
                message_text = updates[0]['message']['text']
                mssg = None
                image = None

                print(message_text)

                if message_text == '/fullreport' or message_text == '/start':
                    if str(user_id) == config('USER_ID'):
                        print("aca")
                        mssg = binance_info.binance()
                        image = image_info.generate_report(
                            binance_info.get_coins(), binance_info.get_prices(),
                            binance_info.get_balance())
                        image = image_info.get_image()
                        image, err = Imgur.upload_image(image=image)

                        if err:
                            mssg += f"\n{image}\n"
                            image = None

                    else:
                        mssg = "Sorry this is a personal bot, you can't access it, but you can implement your own bot using the source code :) https://github.com/Daniel-Alba15/Telegram-Crypto-Bot"
                        image = None

                    self._send_message(mssg, chat_id, image)

                else:
                    print("Texto incorrecto")
                
                offset += 1

