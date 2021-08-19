import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
from ibapi.order_state import OrderState
from time import sleep

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
        self.check_orders()
        print("Executing requests ... finished")

    # def orderOperations_req(self):
    #     # Requesting all open orders
    #     # ! [reqallopenorders]
    #     self.reqAllOpenOrders()
    #     # ! [reqallopenorders]
    #
    # def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
    #               orderState: OrderState):
    #     super().openOrder(orderId, contract, order, orderState)
    #     # print("OpenOrder. PermId: ", order.permId, "ClientId:", order.clientId, " OrderId:", orderId,
    #     #       "Account:", order.account, "Symbol:", contract.symbol, "SecType:", contract.secType,
    #     #       "Exchange:", contract.exchange, "Action:", order.action, "OrderType:", order.orderType,
    #     #       "TotalQty:", order.totalQuantity, "CashQty:", order.cashQty,
    #     #       "LmtPrice:", order.lmtPrice, "AuxPrice:", order.auxPrice, "Status:", orderState.status)
    #
    #     order.contract = contract
    #     self.permId2ord[order.permId] = order
    #     self.data.append([order.permId, OrderId, contract.symbol, contract.secType, contract.exchange, order.action,
    #                       order.orderType,order.totalQuantity, order.lmtPrice, orderState.status])
    #     self.df = pd.DataFrame(self.data, columns=['Account', 'OrderID', 'Ticker', 'SecType', 'Exchange', 'Order', 'Type', 'Qty',
    #                                                'Price', 'Status'])
    #
    # def openOrderEnd(self):
    #     super().openOrderEnd()
    #     print("OpenOrderEnd")
    #     self.sendOrder('BUY')
    #     sleep(3)
    #     self.check_orders()

    def sendOrder(self, action):
        self.contract.symbol = 'NQ'
        self.contract.secType = 'FUT'
        self.contract.exchange = 'GLOBEX'
        self.contract.currency = 'USD'
        self.contract.lastTradeDateOrContractMonth = "202109"

        order = Order()
        order.action = action
        order.totalQuantity = 1
        order.orderType = "LMT"
        order.lmtPrice = 14900
        self.placeOrder(self.nextOrderId(), self.contract, order)
        # self.placeOrder(248, self.contract, order)

    def check_orders(self):
        self.sendOrder('BUY')
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()