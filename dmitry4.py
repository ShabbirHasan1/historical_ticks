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
app.connect('127.0.0.1', 7497, 250)

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
eurusd_contract.lastTradeDateOrContractMonth = "202106"

# Request historical candles
counter = 0
while counter < 3:
    app.reqHistoricalData(1, eurusd_contract, '20210525 06:20:57', '1 D', '1 hour', 'TRADES', 0, 2, False, [])
    time.sleep(2)
    df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
    df['DateTime'] = df['DateTime'].astype(int)
    time.sleep(2)
    pick_time = df['DateTime'].values[2]
    print(datetime.datetime.fromtimestamp(pick_time).strftime("%Y%m%d %H:%M:%S"))
    # print(df['DateTime'].values[2])
    counter = counter + 1
    time.sleep(5)  # sleep to allow enough time for data to be returned


# Working with Pandas DataFrames

df1 = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
df1['DateTime'] = pandas.to_datetime(df1['DateTime'], unit='s')
df1.to_csv('EURUSD_Hourly.csv')

print(df1)

app.disconnect()