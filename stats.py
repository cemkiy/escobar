from bitfinex.client import Client
import datetime
from utils import Utils
from real_environment import real_environment


class Stats():
    def __init__(self):
        self.renv = real_environment.RealEnvironment()
        self.symbol = self.renv.get_env_or_default("coin_symbol", "btcusd")
        self.client = Client()
        self.ticker = self.client.ticker(self.symbol)
        self.today = self.client.today(self.symbol)
        self.stats = self.client.stats(self.symbol)
        self.utils = Utils()

    def process_volume_stats(self):
        daily_volume = self.stats[0].volume
        weekly_volume = self.stats[1].volume
        montly_volume = self.stats[2].volume

        avg_weekly_volume = montly_volume / 4
        avg_daily_volume = weekly_volume / 7

        weekly_trend = False
        daily_trend = False

        if weekly_volume >= avg_weekly_volume:
            weekly_trend = True
        if daily_volume >= avg_daily_volume:
            daily_trend = True

        if weekly_trend and daily_trend:
            return 'power'
        elif weekly_trend or daily_trend:
            return 'normal'
        else:
            return 'weak'

    def process_from_the_bottom_to_the_top(self):
        max_price = self.today.high
        min_price = self.today.low

        increment_percent = self.utils.percentage(
            self.ticker.last_price - min_price, min_price)
        decrement_percent = self.utils.percentage(
            max_price - self.ticker.last_price, max_price)

        if increment_percent > decrement_percent:
            return 'power'
        elif increment_percent == decrement_percent:
            return 'normal'
        else:
            return 'weak'

    def process_week(self):
        weekno = datetime.datetime.today().weekday()

        if weekno < 5:
            # weekday
            return 'power'
        else:
            # weak
            return 'weak'
