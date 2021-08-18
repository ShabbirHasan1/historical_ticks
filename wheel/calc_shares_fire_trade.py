import math
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from datetime import datetime
from ibapi.order import Order
import pause
import yfinance as yf
from time import sleep

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.contract = Contract()
        self.data = []
        self.df = pd.DataFrame()
        self.data1 = []
        self.df1 = pd.DataFrame()
        self.recent_price = 0
        self.cash_value = 0
        self.num_shares = 0
        self.safety_num_shares = 0
        self.shares_to_buy = 0
        self.num_contracts = 0
        self.ticker = None

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

        # we can start now
        self.start()

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    def start(self):

   #     self.tickDataOperations_req()
        self.accountOperations_req()
        # self.check_and_send_order()
        print("Executing requests ... finished")

    def accountOperations_req(self):
        # Requesting accounts' summary
        # ! [reqaaccountsummary]
        self.reqAccountSummary(9002, "All", "$LEDGER")
        # ! [reqaaccountsummary]

    # ! [accountsummary]
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        # print("AccountSummary. ReqId:", reqId, "Account:", account,
        #       "Tag: ", tag, "Value:", value, "Currency:", currency)
        self.data1.append([tag, value])
        self.df1 = pd.DataFrame(self.data1, columns=['Account', 'Value'])
        if len(self.df1) == 24:
            # print(self.df1)
            self.df1.to_csv('acct_value.csv')
            self.cash_value = self.df1.loc[2, 'Value']
            print(f'cash value: {self.cash_value}')
            self.check_and_send_order()

    def sendOrder(self, action):
        self.contract.symbol = 'QQQ'
        self.contract.secType = 'STK'
        self.contract.exchange = 'SMART'
        self.contract.currency = 'USD'

        order = Order()
        order.action = action
        order.totalQuantity = self.shares_to_buy
        order.orderType = "MKT"
        self.placeOrder(self.nextOrderId(), self.contract, order)

    def check_and_send_order(self):
        trade_time = datetime(2021, 8, 18, 12, 8, 0)
        pause.until(trade_time)
        self.check_price()
        sleep(1)
        self.calc_contracts()
        sleep(1)
        print(f'Buy {self.shares_to_buy} {self.ticker}')
        sleep(1)
        self.sendOrder('BUY')
        print(f'BOT {self.shares_to_buy} {self.ticker} at {trade_time}')
        self.disconnect()

    def check_price(self):
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # https://pypi.org/project/yfinance
        self.ticker = "QQQ"
        data = yf.download(tickers=self.ticker, period="1d", interval='5m')
        df1 = pd.DataFrame(data)
        # print(df1)
        self.recent_price = df1['Close'].iloc[-1]
        print(f'recent price: {self.recent_price}')

    def calc_contracts(self):
        # if len(self.data) > 0:
        # self.recent_price = sum(self.data) / len(self.data)
        # self.check_price()
        self.num_shares = float(self.cash_value) / (self.recent_price)
        self.safety_num_shares = 0.75 * self.num_shares
        self.shares_to_buy = math.floor(self.safety_num_shares / 100) * 100
        self.num_contracts = self.shares_to_buy / 100
        print(f'shares to trade: {self.shares_to_buy}')

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()