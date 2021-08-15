import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
import time
import yfinance as yf

# https://stackoverflow.com/questions/11523918/python-start-a-function-at-given-time
# https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.contract = Contract()
        self.recent_price = 0

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
        self.check_and_send_order()
        print("Executing requests ... finished")

    def check_price(self):
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # https://pypi.org/project/yfinance
        ticker = "NQ=F"
        data = yf.download(tickers=ticker, period="1d", interval='5m')
        df1 = pd.DataFrame(data)
        # print(df1)
        self.recent_price = df1['Close'].iloc[-1]
        print(f'recent price: {self.recent_price}')

    def sendOrder(self, action):
        # Create contract object
        self.contract.symbol = 'NQ'
        self.contract.secType = 'FUT'
        self.contract.exchange = 'GLOBEX'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "202109"

        order = Order()
        order.action = action
        order.totalQuantity = 1
        order.orderType = "MKT"
        self.placeOrder(self.nextOrderId(), self.contract, order)

    def check_and_send_order(self):
        counter = 0
        while counter < 25:
            counter += 1
            self.check_price()
            if self.recent_price > 15120:
                self.sendOrder('SELL')
            elif self.recent_price < 15100:
                self.sendOrder('BUY')
            time.sleep(10)
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=108)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(), app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()