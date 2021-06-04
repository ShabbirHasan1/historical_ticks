from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

# https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

        # self.data = []  # Initialize variable to store candle

    def historicalTicksLast(self, reqId: int, ticks,
                            done: bool):
        for tick in ticks:
            print("HistoricalTickLast. ReqId:", reqId, tick)
            # self.data.append(tick)

    # def historicalData(self, reqId, bar):
    #     print(f'Time: {bar.date} Close: {bar.close}')
    #     self.data.append([bar.date, bar.close])


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7497, 12)

# Start the socket in a thread
# api_thread = threading.Thread(target=run_loop, daemon=True)
# api_thread.start()

# time.sleep(1)  # Sleep interval to allow time for connection to server

# Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'EUR'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'
eurusd_contract.currency = 'USD'

# Request historical candles
app.reqHistoricalTicks(18001, eurusd_contract,
                        "20210527 09:39:33", "", 1000, "TRADES", 1, True, [])
# app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])

# time.sleep(5)  # sleep to allow enough time for data to be returned

# Working with Pandas DataFrames
# import pandas
#
# df = pandas.DataFrame(app.data)
# # df['DateTime'] = pandas.to_datetime(df['DateTime'], unit='s')
# df.to_csv('EURUSD_Hourly.csv')
#
# print(df)

# app.disconnect()
