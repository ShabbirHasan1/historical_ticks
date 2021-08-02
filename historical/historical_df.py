import pandas as pd
from ibapi.utils import iswrapper
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from time import sleep

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.data = []  # Initialize variable to store candle
        self.contract = Contract()
        self.cols = ['data', 'open', 'high', 'low', 'close', 'volume']
        self.df = pd.DataFrame(columns=self.cols)

    def nextValidId(self, orderId: int):
        # we can start now
        self.start()

    def start(self):
        self.historicalDataOperations_req()
        print("Executing requests ... finished")

    def historicalDataOperations_req(self):

        self.contract.symbol = 'NQ'
        self.contract.secType = 'FUT'
        self.contract.exchange = 'GLOBEX'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "202109"
        self.reqHistoricalData(4103, self.contract, '',
                                   "1 D", "1 hour", "TRADES", 0, 1, True, []) # the first 0 means after hours

    # https://stackoverflow.com/questions/10715965/create-a-pandas-dataframe-by-appending-one-row-at-a-time

    def historicalData(self, reqId: int, bar: BarData):
        #self.data.append([reqId, bar])
        self.df.loc[len(self.df)] = [bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume]
        self.displ_hist()
        #print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        #print(self.df)
        #self.df.to_csv('history1.csv')

    def displ_hist(self):
        # num_rows = len(self.df)
        if len(self.df) == 19:
            print(self.df)
            sleep(2)
            self.df.to_csv('history2.csv')
        self.disconnect()  # this is what allows the loop to keep going


def main():
    counter = 0
    while counter < 4:
        app = TestApp()
        app.connect('127.0.0.1', 7497, 120)
        app.run()
        sleep(3)
        counter = counter + 1

    # app = TestApp()
    # app.connect("127.0.0.1", port=7497, clientId=105)
    # print("serverVersion:%s connectionTime:%s" % (app.serverVersion(), app.twsConnectionTime()))
    # app.run()

if __name__ == "__main__":
    main()

