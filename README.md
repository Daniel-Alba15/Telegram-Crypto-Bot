# Telegram-Crypto-Bot

This is a telegram bot that syncs with your spot wallet in [Binance](https://www.binance.com/) and generates report graphs according to your profits or loses using matplotlib and pandas librarys.


## Installation

Clone this repository and install requiermentes

```bash
git clone https://github.com/Daniel-Alba15/Telegram-Crypto-Bot.git
cd Telegram-Crypto-Bot/
pip install -r requirements.txt
```

## Usage

Unfortunately Binance doesn't have Oauth authentication available yet, so you'll have to generate your own [Binance](https://www.binance.com/my/settings/api-management), [Telegram] (https://core.telegram.org/bots) and [Imgur](https://apidocs.imgur.com) api keys.

Do not forget to save all of this on your ```.env``` file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
