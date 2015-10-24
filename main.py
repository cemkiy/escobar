# author: cemkiy (gitlab and github username)
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

        self._btcturk = Btcturk("app-id", "secret")

        self.btcturk_data = self._btcturk.ticker()
        self.account_data = self._btcturk.balance()

        self.btcturk_transactions = self.get_transactions()

        self.revenue_sell_price = 0
        self.loss_sell_price = 0

        self.yo = yopy.Yo('45f44dae-6dbb-4f2c-977c-3acb71a84432')


    def get_transactions(self):
        control = False
        while True:
            if control == True:
                break
            try:
                transactions = self._btcturk.transactions(limit=2)
                control = True
            except Exception as e:
                print e
        return transactions

    def guess_what(self):
        totality_guess = 0
        if self.btcturk_data['open'] <= self.btcturk_data['ask']:
            totality_guess += 1
        if self.btcturk_data['open'] <= self.btcturk_data['average']:
            totality_guess +=1
        if abs(float(self.btcturk_data['ask']) - float(self.btcturk_data['high'])) <= abs(float(self.btcturk_data['average']) - float(self.btcturk_data['high'])):
            totality_guess += 1
        if (abs(float(self.btcturk_data['ask']) - float(self.btcturk_data['open'])) * 100) / float(self.btcturk_data['open']) > 1.04:
            totality_guess += 1
        print 'guess_what', totality_guess
        if totality_guess > 3:
            return True
        else:
            return False


    def count_rates(self):
        out_of_my_pocket =  self.out_of_my_pocket()
        self.revenue_sell_price = out_of_my_pocket + (out_of_my_pocket / 100)
        print 'revenue sell price', self.revenue_sell_price
        self.loss_sell_price = out_of_my_pocket - (out_of_my_pocket / 100)
        print 'loss sell price', self.loss_sell_price


    def out_of_my_pocket(self):
        total_money = 0
        for transaction in self.btcturk_transactions:
            print "%s: %s" % (transaction['operation'], transaction['currency'])
            total_money += abs(float(transaction['currency']))
        print 'out of my pocket', total_money
        return total_money


    def sell_btc(self):
        print 'sell btc'
        control = False
        while True:
            if control == True:
                break
            try:
                self._btcturk.sell_with_market_order(self.account_data['bitcoin_available'])
                control = True
            except Exception as e:
                print e



    def buy_btc(self):
        print 'buy btc'
        control = False
        while True:
            if control == True:
                break
            try:
                self._btcturk.buy_with_market_order(self.account_data['money_available'])
                control = True
            except Exception as e:
                print e



    def plata_o_plomo(self):
        if float(self.account_data['bitcoin_available']) > 0:
            print 'BTC transaction'
            self.count_rates()
            btc_now_price = float(self.btcturk_data['bid']) * float(self.account_data['bitcoin_available'])
            if btc_now_price > self.revenue_sell_price:
                self.sell_btc()
                self.yo.yoall('https://www.youtube.com/watch?v=lqn8L3JIALY')
            elif btc_now_price <= self.loss_sell_price:
                self.sell_btc()
                self.yo.yoall('https://www.youtube.com/watch?v=dH05wYoQj9k')
        else:
            print 'TRY transaction'
            if self.guess_what():
                self.buy_btc()
                self.yo.yoall()


    def update(self):
        self.btcturk_data = self._btcturk.ticker()
        self.account_data = self._btcturk.balance()
        self.btcturk_transactions = self.get_transactions()


    def cron_try(self):
        self.yo.yoall()



run = main()
while True:
    run.update()
    run.plata_o_plomo()
    time.sleep(600)
