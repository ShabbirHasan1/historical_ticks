from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer
import pandas as pd
import numpy as np

# from https://github.com/algothinktank/ibkr

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.df = pd.DataFrame(columns=['symbol', 'security_type', 'position'])

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId):
        self.start()

    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
              contract.exchange,
              "Position", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:",
              averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

        self.df.loc[len(self.df)] = [contract.symbol, contract.secType, position]
        df_new = pd.DataFrame()
        self.df.to_csv('position.csv')
        #print(self.df)
        df_new['new_position'] = self.df['position']
        df_new['new_security_type'] = self.df['security_type']
        #df_new['check_position'] = np.where(self.df['position'] > 200, 1, 0)

        df_new['check_position'] = np.where(['new_security_type'] == 'STK', 1, 0)
        print(df_new)

    def start(self):
        self.reqAccountUpdates(True, "")

    def stop(self):
        self.reqAccountUpdates(False, "")
        self.done = True
        self.disconnect()

#execute the classes
def main():

    app2 = TestApp()
    app2.connect("127.0.0.1", 7497, 9)  # IB Gateway PaperTrading
    Timer(3, app2.stop).start()
    app2.run()



if __name__ == "__main__":
    main()