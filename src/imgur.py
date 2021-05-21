from decouple import config
import requests
import logging

class Imgur():

    @staticmethod
    def upload_image(image):
        URL = "https://api.imgur.com/3/image"
        data = {'image': image}
        headers = {
            'Authorization':  'Client-ID ' + config("CLIENT_ID")
        }

        try:
            logging.info("Making a request to imgur")
            res = requests.post(URL, headers=headers, data=data)
        except requests.exceptions.ConnectionError as e:
            logging.error(e)
            return "Something went wrong uploading the image, pleas trya again", True

        return res.json()['data']['link'], False
