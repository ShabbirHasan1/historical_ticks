import math
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
import datetime

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.contract = Contract()
        self.data = []
        self.df = pd.DataFrame()
        self.data1 = []
        self.df1 = pd.DataFrame()
        self.recent_price = 0
        self.cash_value = 0
        self.num_shares = 0
        self.safety_num_shares = 0
        self.shares_to_buy = 0
        self.num_contracts = 0

    def nextValidId(self, orderId: int):
        # we can start now
        self.start()

    def start(self):

        self.tickDataOperations_req()
        self.accountOperations_req()
        print("Executing requests ... finished")

    def accountOperations_req(self):
        # Requesting accounts' summary
        # ! [reqaaccountsummary]
        self.reqAccountSummary(9002, "All", "$LEDGER")
        # ! [reqaaccountsummary]

    # ! [accountsummary]
    def accountSummary(self, reqId: int, account: str, tag: str, value: str,
                       currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        # print("AccountSummary. ReqId:", reqId, "Account:", account,
        #       "Tag: ", tag, "Value:", value, "Currency:", currency)
        self.data1.append([tag, value])
        self.df1 = pd.DataFrame(self.data1, columns=['Account', 'Value'])
        if len(self.df1) == 24:
            # print(self.df1)
            self.df1.to_csv('acct_value.csv')
            self.cash_value = self.df1.loc[2, 'Value']

    def tickDataOperations_req(self):
        # Create contract object
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
        print('Time:', datetime.datetime.fromtimestamp(time),
              "Price:", "{:.2f}".format(price),
              'Size:', size, self.recent_price,
              self.cash_value,
              self.num_shares,
              self.shares_to_buy,
              self.num_contracts)
        self.data.append(price)
        if len(self.data) > 5:
            self.data.pop(0)
        if len(self.data) > 0:
            self.recent_price = sum(self.data) / len(self.data)
            self.num_shares = float(self.cash_value) / (self.recent_price / 100) # get rid of / 100
            self.safety_num_shares = 0.75 * self.num_shares
            self.shares_to_buy = math.floor(self.safety_num_shares / 100) * 100
            self.num_contracts = self.shares_to_buy / 100

def main():
    app = TestApp()
    app.connect("127.0.0.1", port=7497, clientId=102)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
    app.run()

if __name__ == "__main__":
    main()