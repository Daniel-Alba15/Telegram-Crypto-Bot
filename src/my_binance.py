from decouple import config
from binance.client import Client
from binance.exceptions import BinanceAPIException


class Binance():
    def __init__(self):
        self.client = Client(config("API_KEY"), config("API_SECRET"))
        self.info = self.client.get_account()
        self.coinss = []
        self.prices = []
        self.balance = []

    def _get_trades(self, coin):
        """Return a list of trades based on the coin agains USDT or/and BUSD"""
        if coin != "USDT" and coin != "BUSD":
            trades = self.client.get_my_trades(symbol=f"{coin}USDT")
            try:
                trades += self.client.get_my_trades(symbol=f"{coin}BUSD")
            except BinanceAPIException:
                print(f"[ERROR]: There is no match for {coin}/BUSD")

            return trades

        return None

    def _get_coins(self, data):
        """Return a list of coins based on the spot wallet"""
        coins = []
        for d in data:
            if float(d['free']) > 0.0:
                coins.append(d['asset'])

        return coins

    def _get_quantity_price(self, trade):
        """"Return quantity and price for the actual buy trade"""
        quantity, price = 0, 0
        if trade['isBuyer'] == True:
            quantity, price = float(trade['qty']), float(trade['price'])

        return quantity, price

    def _get_total(self, buy_price, current_price, quantity):
        """Retrun the total profit"""
        total = (current_price * quantity) - (buy_price * quantity)

        return total

    def get_coins(self):
        return self.coinss

    def get_balance(self):
        return self.balance

    def get_prices(self):
        return self.prices

    def binance(self):
        balances = self.info['balances']

        coins = self._get_coins(balances)
        message = ""

        for coin in coins:
            trades = self._get_trades(coin)

            if trades:
                avg_price = float(self.client.get_avg_price(
                    symbol=f"{coin}USDT")["price"])
                total = 0
                asset_balance = self.client.get_asset_balance(asset=coin)[
                    'free']

                for trade in trades:
                    quantity, price = self._get_quantity_price(trade)

                    if quantity > 0.0 and price > 0.0:
                        total += self._get_total(buy_price=price,
                                                 current_price=avg_price, quantity=quantity)

                self.prices.append(float(total))
                self.coinss.append(coin)
                self.balance.append(float(asset_balance))

                message += f"{coin}, you have: {asset_balance}\nYou buy at {price}\nCurrent price {avg_price}\nYou are winning: {total}\n\n"

        return message
