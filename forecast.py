from coinmarketcap import Market
from real_environment import real_environment
import datetime


class Forecast:
    def __init__(self):
        self.renv = real_environment.RealEnvironment()
        self.coinmarketcap = Market()
        self.ticker = self.coinmarketcap.ticker(self.renv.get_env_or_default("coin_name", "bitcoin"),
            convert=self.renv.get_env_or_default("currency", "USD"))[0]
        '''
        [
            {
                "id": "bitcoin",
                "name": "Bitcoin",
                "symbol": "BTC",
                "rank": "1",
                "price_usd": "11710.0",
                "price_btc": "1.0",
                "24h_volume_usd": "19160900000.0",
                "market_cap_usd": "196848905750",
                "available_supply": "16810325.0",
                "total_supply": "16810325.0",
                "max_supply": "21000000.0",
                "percent_change_1h": "-0.57",
                "percent_change_24h": "14.41",
                "percent_change_7d": "-15.59",
                "last_updated": "1516281264",
                "price_eur": "9576.50826",
                "24h_volume_eur": "15669898985.4",
                "market_cap_eur": "160984216216"
            }
        ]
        '''
        self.stats = self.coinmarketcap.stats(convert=self.renv.get_env_or_default("currency", "USD"))
        '''
        {
            "total_market_cap_usd": 572724110011.0,
            "total_24h_volume_usd": 62123365544.0,
            "bitcoin_percentage_of_market_cap": 34.29,
            "active_currencies": 895,
            "active_assets": 535,
            "active_markets": 7597,
            "last_updated": 1516281565,
            "total_market_cap_eur": 468377213511.0,
            "total_24h_volume_eur": 50804861082.0
            }
        '''

    def update(self):
         self.ticker = self.coinmarketcap.ticker(self.renv.get_env_or_default("coin_name", "bitcoin"),
             convert=self.renv.get_env_or_default("currency", "USD"))
         self.stats = self.coinmarketcap.stats(convert=self.renv.get_env_or_default("currency", "USD"))

    def trend_by_perc(self):
        score = 0
        if self.ticker['percent_change_1h'] > self.ticker['percent_change_24h']:
            score += 1
        if self.ticker['percent_change_24h'] > self.ticker['percent_change_7d']:
            score += 1
        if score > 2:
            return 1
        elif score > 1:
            return 0
        else:
            return -1

    def trend_by_weekdays(self):
        weekno = datetime.datetime.today().weekday()

        if weekno < 5:
            # weekday
            return 0
        else:
            # weekend
            return -1
