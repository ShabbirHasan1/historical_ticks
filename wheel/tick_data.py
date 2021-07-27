import logging
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
import datetime

eurusd_contract = Contract()

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.permId2ord = {}
        self.contract = Contract()
        self.data = []  # Initialize variable to store candle
        self.df = pd.DataFrame()

    def nextValidId(self, orderId: int):

        # we can start now
        self.start()

    def start(self):
        self.tickDataOperations_req()
        print("Executing requests ... finished")

    def tickDataOperations_req(self):
        # Create contract object

        eurusd_contract.symbol = 'NQ'
        eurusd_contract.secType = 'FUT'
        eurusd_contract.exchange = 'GLOBEX'
        eurusd_contract.currency = 'USD'
        eurusd_contract.lastTradeDateOrContractMonth = "202109"

        self.reqTickByTickData(19002, eurusd_contract, "AllLast", 0, False)

    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast, exchange: str,
                          specialConditions: str):
        print('Time:', datetime.datetime.fromtimestamp(time),
              "Price:", "{:.2f}".format(price),
              'Size:', size)

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()