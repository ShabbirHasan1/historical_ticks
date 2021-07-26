import logging
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import Order
from ibapi.order_state import OrderState

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
        self.orderOperations_req()
        print("Executing requests ... finished")

    def orderOperations_req(self):
        # Requesting all open orders
        self.reqAllOpenOrders()
        self.reqCompletedOrders(False)

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
    #     self.data.append([order.permId, contract.symbol, contract.secType, contract.exchange, order.action,
    #                       order.orderType,order.totalQuantity, order.lmtPrice, orderState.status])
    #     self.df = pd.DataFrame(self.data)
    #     if len(self.df) == 2:
    #         print(self.df)
    #     self.df.to_csv('open_orders.csv')
    #
    #     # ! [openorder]
    #
    # # ! [openorderend]
    # def openOrderEnd(self):
    #     super().openOrderEnd()
    #     print("OpenOrderEnd")

    # ! [orderstatus]
    def completedOrder(self, contract: Contract, order: Order,
                  orderState: OrderState):
        super().completedOrder(contract, order, orderState)
        print("CompletedOrder. PermId:", order.permId, "ParentPermId:", "Account:", order.account,
              "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
              "Action:", order.action, "OrderType:", order.orderType, "TotalQty:", order.totalQuantity,
              "CashQty:", order.cashQty, "FilledQty:", order.filledQuantity,
              "LmtPrice:", order.lmtPrice, "AuxPrice:", order.auxPrice, "Status:", orderState.status,
              "Completed time:", orderState.completedTime, "Completed Status:" + orderState.completedStatus)
    # ! [completedorder]

    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", filled,
              "Remaining:", remaining, "AvgFillPrice:", avgFillPrice,
              "PermId:", permId, "ParentId:", parentId, "LastFillPrice:",
              lastFillPrice, "ClientId:", clientId, "WhyHeld:",
              whyHeld, "MktCapPrice:", mktCapPrice)
        self.data.append([orderId, status, filled, remaining, avgFillPrice,
                          permId, lastFillPrice, mktCapPrice])
        self.df = pd.DataFrame(self.data)
        # if len(self.df) == 2:
        print(self.df)
        self.df.to_csv('open_orders.csv')

        self.disconnect()
    # ! [orderstatus]

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()