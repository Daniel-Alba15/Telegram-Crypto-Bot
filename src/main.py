from my_binance import Binance
from telegram import Telegram
from image import Image
from imgur import Imgur
from decouple import config


offset = 0
telegram = Telegram()
my_binance = Binance()
my_image = Image()


def send_text(chat_id):
    mssg = my_binance.binance()
    telegram.send_message(mssg, chat_id)


def send_image(chat_id):
    image = my_image.generate_report(
        my_binance.get_coins(), my_binance.get_prices(),
        my_binance.get_balance())
    image = my_image.get_image()
    image, err = Imgur.upload_image(image=image)

    if err:
        telegram.send_message(
            "There was a problem with the image, please try again", chat_id)
    else:
        telegram.send_message(chat_id=chat_id, image=image)


while (True):

    updates = telegram.get_updates(offset)

    if updates:
        if offset == 0:
            offset = updates[0]["update_id"]

        user_id = updates[0]["message"]["from"]["id"]
        chat_id = updates[0]["message"]["chat"]["id"]
        message_text = updates[0]["message"]["text"]

        if message_text.startswith("/"):
            if str(user_id) == config("USER_ID"):
                if message_text == "/fullreport" or message_text == "/start":
                    send_text(chat_id)
                    send_image(chat_id)
                elif message_text == "/text":
                    send_text(chat_id)
                elif message_text == "/image":
                    send_image(chat_id)
            else:
                mssg = "Sorry this is a personal bot, you can't access it, but you can implement your own bot using the source code :) https://github.com/Daniel-Alba15/Telegram-Crypto-Bot"
                telegram.send_message(mssg, chat_id)

        offset += 1
