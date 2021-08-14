import logging
from datetime import datetime, timedelta
import time


import pandas as pd

from ibapi.utils import iswrapper

from ContractSamples import ContractSamples

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport

# https://stackoverflow.com/questions/41510945/interactive-brokers-obtain-historical-data-of-opt-midpoint-and-trades
# https://groups.io/g/twsapi/topic/data_for_expired_contracts_no/4042776?p=

class TestApp(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        # ! [socket_init]
        self.nKeybInt = 0
        self.started = False
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.globalCancelOnly = False
        self.simplePlaceOid = None
        self._my_errors = {}
        self.data = []  # Initialize variable to store candle
        self.contract = Contract()
        self.i = 0
        self.df = pd.DataFrame()

    @iswrapper
    # ! [connectack]
    def connectAck(self):
        if self.asynchronous:
            self.startApi()

    # ! [connectack]

    @iswrapper
    # ! [nextvalidid]
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)

        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
        # ! [nextvalidid]

        # we can start now
        self.start()

    def start(self):
        if self.started:
            return

        self.started = True

        if self.globalCancelOnly:
            print("Executing GlobalCancel only")
            self.reqGlobalCancel()
        else:
            print("Executing requests")
            # self.tickDataOperations_req()
            self.historicalDataOperations_req()
            print("Executing requests ... finished")

    def keyboardInterrupt(self):
        self.nKeybInt += 1
        if self.nKeybInt == 1:
            self.stop()
        else:
            print("Finishing test")
            self.done = True

    def stop(self):
        print("Executing cancels")
        self.tickByTickOperations_cancel()

        print("Executing cancels ... finished")

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    @iswrapper
    # ! [error]
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        print("Error. Id:", reqId, "Code:", errorCode, "Msg:", errorString)
        errormsg = "IB error id %d errorcode %d string %s" % (reqId, errorCode, errorString)
        self._my_errors = errormsg

    @iswrapper
    def winError(self, text: str, lastError: int):
        super().winError(text, lastError)

#    @printWhenExecuting
#     def historicalTicksOperations(self):
#         # ! [reqhistoricalticks]
#
#         self.reqHistoricalTicks(18001, ContractSamples.USOptionContract(),
#                                 '20210722 09:39:33', "", 50, "TRADES", 1, True, [])
#

    def historicalDataOperations_req(self):

        chain = [134, 135, 136]
        for self.i in chain:
            self.contract.symbol = "TQQQ"
            self.contract.secType = "OPT"
            self.contract.exchange = "SMART"
            self.contract.currency = "USD"
            self.contract.lastTradeDateOrContractMonth = "20210813"
            self.contract.strike = self.i
            self.contract.right = "C"
            self.contract.multiplier = "100"
            queryTime = (datetime.today() - timedelta(days=0)).strftime("%Y%m%d %H:%M:%S")
            self.reqHistoricalData(4103, self.contract, queryTime,
                                   "5 D", "5 mins", "MIDPOINT", 1, 1, False, [])

            # https://interactivebrokers.github.io/tws-api/historical_bars.html

    def historicalData(self, reqId: int, bar: BarData):
        self.data.append([bar])
        # print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        self.df = pd.DataFrame(self.data)
        print(self.df)
        self.df.to_csv('history.csv')
        # if len(self.df) == 44:  # check number of rows and then this will be it
        # self.disconnect()

def main():

    app = TestApp()
    try:

        # ! [connect]
        app.connect("127.0.0.1", port=7497, clientId=102)
        # ! [connect]
        print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                      app.twsConnectionTime()))
        # ! [clientrun]
        app.run()
        # ! [clientrun]
    except:
        raise


if __name__ == "__main__":
    main()