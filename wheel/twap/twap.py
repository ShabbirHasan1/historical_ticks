import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
from datetime import datetime
import pause

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.contract = Contract()
        self.data = []  # Initialize variable to store candle
        self.df = pd.DataFrame()

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
        start_time = datetime(2021, 7, 28, 5, 11, 0)
        end_time = datetime(2021, 7, 28, 5, 12, 0)
        # start_time = datetime(2021, 7, 27, 9, 30, 0)
        # end_time = datetime(2021, 7, 27, 16, 00, 0)
        diff = end_time - start_time
        print(diff)
        num_slices = 4
        time_slice = diff / num_slices
        print(time_slice)
        first_slice = start_time + time_slice
        print(first_slice)
        list_of_times = []
        i = 1
        for i in range(1, num_slices):
            new_time = start_time + time_slice
            list_of_times.append(new_time)
            start_time = new_time
            i += 1
        print(list_of_times)

        time_counter = 0
        for j in list_of_times:
            trade_time = list_of_times[time_counter]
            pause.until(trade_time)
            self.sendOrder('BUY')
            print(f'BUY at {trade_time}')
            time_counter += 1

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=108)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()