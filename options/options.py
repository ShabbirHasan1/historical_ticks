# https://stackoverflow.com/questions/62371672/python-interactive-brokers-api-very-slow-for-historical-option-prices

import time
import pandas as pd
import collections
import datetime as dt

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData


class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = collections.defaultdict(list)
        self.df = pd.DataFrame()

    def error(self, reqId: int, errorCode: int, errorString: str):
        print("Error: ", reqId, "", errorCode, "", errorString)

    def historicalData(self, reqId: int, bar: BarData):
        self.data["date"].append(bar.date)
        self.data["price"].append(bar.close)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        self.df = pd.DataFrame.from_dict(self.data)
        self.disconnect()
        print("finished")


def get_option_histo_prices_test(ticker: str, expiry: str, strike: str):
    app = TestApp()
    app.connect("127.0.0.1", 7497, 3)

    time.sleep(1)

    contract = Contract()
    contract.secType = "OPT"
    contract.right = "C"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.multiplier = "100"

    contract.symbol = ticker
    contract.lastTradeDateOrContractMonth = expiry
    contract.strike = strike

    app.reqHistoricalData(1, contract, "", "4 M", "8 hours", "TRADE", 1, 1, False, [])

    app.run()

    return app.df


ticker = "AAPL"
expiry = "20200619"
start_time_initial = time.time()
for strike in ["300", "280", "240", "220", "180", "160"]:
    start_time = time.time()
    prices = get_option_histo_prices_test(ticker, expiry, strike)
    end_time = time.time()
    print(end_time - start_time)

end_time_final = time.time()
print("it took", end_time_final - start_time_initial)