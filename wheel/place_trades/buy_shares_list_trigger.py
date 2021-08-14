from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
import time


# https://stackoverflow.com/questions/11523918/python-start-a-function-at-given-time
# https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.contract = Contract()

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
        counter = 0
        sample_list = [3, 5, 6, 7, 8, 9, 10, 40, 3, 6, 7 ,8]
        for i in sample_list:
            counter += 1
            print(i)
            time.sleep(3)
            if counter == 3:
                self.sendOrder('SELL')
            elif counter == 6:
                self.sendOrder('BUY')
        self.disconnect()


def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=108)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()