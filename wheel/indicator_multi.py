import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
import datetime
from finta import TA

MOVING_AVG_PERIOD_LENGTH = 3
MOVING_AVG_PERIOD_LENGTH_1 = 5
TICKS_PER_CANDLE = 4

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.contract = Contract()
        self.data = []
        self.data1 = []
        self.data_counter = 0
        self.data_counter1 = 0
        self.mov_avg_length = MOVING_AVG_PERIOD_LENGTH
        self.mov_avg_length1 = MOVING_AVG_PERIOD_LENGTH_1
        self.ticks_per_candle = TICKS_PER_CANDLE
        self.tick_count = 0
        self.indicator = 0
        self.indicator1 = 0

    def nextValidId(self, orderId: int):
        # we can start now
        self.start()

    def start(self):
        self.tickDataOperations_req()
        # self.accountOperations_req()
        print("Executing requests ... finished")

    def running_list(self, price: float):
        self.data.append(price)
        self.data_counter += 1
        if self.data_counter < self.mov_avg_length:
            return
        while len(self.data) > self.mov_avg_length:
            self.data.pop(0)

    def running_list1(self, price: float):
        self.data1.append(price)
        self.data_counter1 += 1
        if self.data_counter1 < self.mov_avg_length1:
            return
        while len(self.data1) > self.mov_avg_length1:
            self.data1.pop(0)

    def calc_indicator(self):
        df_indicator = pd.DataFrame(self.data, columns=['close'])
        df_indicator['open'] = df_indicator['close']
        df_indicator['high'] = df_indicator['close']
        df_indicator['low'] = df_indicator['close']
        df_indicator['indicator'] = TA.SMA(df_indicator, self.mov_avg_length) # choose indicator here
        self.indicator = df_indicator['indicator'].iloc[-1]

    def calc_indicator1(self):
        df_indicator1 = pd.DataFrame(self.data1, columns=['close'])
        df_indicator1['open'] = df_indicator1['close']
        df_indicator1['high'] = df_indicator1['close']
        df_indicator1['low'] = df_indicator1['close']
        df_indicator1['indicator1'] = TA.SMA(df_indicator1, self.mov_avg_length1) # choose indicator here
        self.indicator1 = df_indicator1['indicator1'].iloc[-1]

    def tickDataOperations_req(self):
        # Create contract object

        # futures contract
        self.contract.symbol = 'NQ'
        self.contract.secType = 'FUT'
        self.contract.exchange = 'GLOBEX'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "202109"

        # Request tick data
        self.reqTickByTickData(19002, self.contract, "AllLast", 0, False)

    # Receive tick data
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast, exchange: str,
                          specialConditions: str):
        print('Candle:', str(self.tick_count // self.ticks_per_candle+1).zfill(3),
              'Tick:', str(self.tick_count % self.ticks_per_candle + 1).zfill(3),
              'Time:', datetime.datetime.fromtimestamp(time),
              "Price:", "{:.2f}".format(price),
              'Size:', size,
              'Indicator:', "{:.2f}".format(self.indicator),
              'Indicator1:', "{:.2f}".format(self.indicator1))
              # 'Data', self.data)
        if self.tick_count % self.ticks_per_candle == self.ticks_per_candle - 1:
            self.running_list(price)
            self.running_list1(price)
            self.calc_indicator()
            self.calc_indicator1()
        self.tick_count += 1

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()