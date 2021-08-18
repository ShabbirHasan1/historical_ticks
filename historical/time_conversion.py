from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from datetime import datetime, timedelta

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.contract = Contract()
        self.now = datetime.now()
        self.current_time = self.now.strftime("%Y%m%d %H:%M:%S")

    def nextValidId(self, orderId: int):

        # we can start now
        self.start()

    def start(self):

        self.historicalDataOperations_req()
        print("Executing requests ... finished")

    # https://interactivebrokers.github.io/tws-api/historical_time_and_sales.html

    def historicalDataOperations_req(self):
        self.contract.symbol = 'NQ'
        self.contract.secType = 'FUT'
        self.contract.exchange = 'GLOBEX'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "202109"

        self.reqHistoricalData(4103, self.contract, self.current_time,
                               "2 D", "5 mins", "TRADES", 0, 1, False, [])

    def historicalData(self, reqId: int, bar: BarData):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        self.disconnect()

def main():
    app = TestApp()
    app.connect('127.0.0.1', 7497, 120)
    app.run()

if __name__ == "__main__":
    main()

