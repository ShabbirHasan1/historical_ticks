import pandas

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import datetime
import threading
import time

# https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []  # Initialize variable to store candle

    def historicalData(self, reqId, bar):
        print(f'Time: {bar.date} Close: {bar.close}')
        self.data.append([bar.date, bar.close])


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7497, 503)

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server

# Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'NQ'
eurusd_contract.secType = 'FUT'
eurusd_contract.exchange = 'GLOBEX'
eurusd_contract.currency = 'USD'
eurusd_contract.lastTradeDateOrContractMonth = "202109"

# Request historical candles
counter = 0
query_time = '20210624 06:20:57'
# while counter < 3:

app.reqHistoricalData(1, eurusd_contract, query_time, '1 D', '5 secs', 'TRADES', 0, 2, False, [])
print(app.data)
#     df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
#     df['DateTime'] = df['DateTime'].astype(int)
#     time.sleep(5)
#     # pick_time = df['DateTime'].values[2]
#     pick_time = df['DateTime'].min()
#     format_pick_time = datetime.datetime.fromtimestamp(pick_time).strftime("%Y%m%d %H:%M:%S")
#     print(format_pick_time)
#     query_time = format_pick_time
#     # print(df['DateTime'].values[2])
#     counter = counter + 1
#     time.sleep(5)  # sleep to allow enough time for data to be returned
#
#
# # Working with Pandas DataFrames
#
# df_final = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
# df_final['DateTime'] = pandas.to_datetime(df_final['DateTime'], unit='s')
# df_sorted = df_final.sort_values(by = 'DateTime')
# df_sorted.to_csv('EURUSD_Hourly.csv')
#
# print(df_sorted)

app.disconnect()