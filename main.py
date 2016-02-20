# author: @cemkiy
# escobar project

from btcturk_client.client import Btcturk
import yopy
import time


class main():

    def __init__(self):
        """
        bid : sell price
        ask : buy price
        """

        self._btcturk = Btcturk("api-key", "api-secret")
        self.btcturk_data = self._btcturk.ticker()
        self.account_data = self._btcturk.balance()

        self.btcturk_transactions = self.get_transactions()

        self.revenue_sell_price = 0
        self.loss_alarm = 0
        self.salable_price = 0
        self.out_of_my_pocket = 0

        self.sell_perm = False

        self.yo = yopy.Yo('45f44dae-6dbb-4f2c-977c-3acb71a84432')

    def get_transactions(self):
        while True:
            try:
                transactions = self._btcturk.transactions(limit=4)
                break
            except Exception as e:
                print e
        return transactions

    def guess_what(self, rate):
        totality_guess = 0
        if ((float(self.btcturk_data['ask']) - float(self.btcturk_data['open'])) * 100) / float(self.btcturk_data['open']) > rate:
            if self.btcturk_data['open'] <= self.btcturk_data['ask']:
                totality_guess += 1
            if self.btcturk_data['open'] <= self.btcturk_data['average']:
                totality_guess += 1
            if abs(float(self.btcturk_data['ask']) - float(self.btcturk_data['high'])) <= abs(float(self.btcturk_data['average']) - float(self.btcturk_data['high'])):
                totality_guess += 1
            print 'guess_what', totality_guess
        if totality_guess >= 2:
            return True
        else:
            return False

    def count_rates(self):
        self.count_out_of_my_pocket()
        self.revenue_sell_price = self.out_of_my_pocket + (self.out_of_my_pocket / 100)
        print 'revenue sell price', self.revenue_sell_price
        self.loss_alarm = self.out_of_my_pocket - ((self.out_of_my_pocket / 100)*20)
        print 'alarm price', self.loss_alarm

    def count_out_of_my_pocket(self):
        self.out_of_my_pocket = 0
        for index, transaction in enumerate(self.btcturk_transactions):
            if transaction['operation'] == "buy" or transaction['operation'] == "commission":
                self.out_of_my_pocket += abs(float(transaction['currency']))
            elif transaction['operation'] == "sell" and index > 0:
                self.out_of_my_pocket -= abs(float(self.btcturk_transactions[index-1]['currency']))
            print 'total', self.out_of_my_pocket
        print 'out of my pocket', self.out_of_my_pocket

    def sell_btc(self):
        print 'sell btc'
        while True:
            try:
                self._btcturk.sell_with_market_order(self.account_data['bitcoin_available'])
                time.sleep(600)
                break
            except Exception as e:
                print e

    def buy_btc(self):
        print 'buy btc'
        self.sell_perm = False
        self.salable_price = 0
        while True:
            try:
                self._btcturk.buy_with_market_order(self.account_data['money_available'])
                break
            except Exception as e:
                print e

    def plata_o_plomo(self):
        if float(self.account_data['bitcoin_available']) > 0:
            print 'BTC transaction'
            self.count_rates()
            btc_now_price = float(self.btcturk_data['bid']) * \
                float(self.account_data['bitcoin_available'])
            print 'BTC now: ', btc_now_price
            if self.sell_perm and btc_now_price < self.salable_price and btc_now_price > self.out_of_my_pocket:
                if self.guess_what(rate=2) == False:
                    self.yo.youser(username='CEMKY', link='https://www.youtube.com/watch?v=XXjf0VG9ORk')
                    self.sell_btc()
            if btc_now_price > self.revenue_sell_price:
                self.sell_perm = True
                self.salable_price = btc_now_price
            if btc_now_price <= self.loss_alarm:
                self.yo.youser(username='CEMKY', location="41.0256377,28.9719802")
        else:
            print 'TRY transaction'
            if self.guess_what(rate=1.04):
                self.buy_btc()
                self.yo.youser(username='CEMKY')

    def update(self):
        while True:
            try:
                self.btcturk_data = self._btcturk.ticker()
                self.account_data = self._btcturk.balance()
                self.btcturk_transactions = self.get_transactions()
                break
            except Exception as e:
                print e

    def cron_try(self):
        self.yo.youser(username='CEMKY', link="https://github.com/cemkiy/escobar")


run = main()
while True:
    try:
        run.update()
        run.plata_o_plomo()
        time.sleep(120)
    except Exception as e:
        self.yo.youser(username='CEMKY', link="https://github.com/cemkiy/escobar")
        print e
