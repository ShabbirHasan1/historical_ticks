import schedule
import time
import pandas as pd
import csv
import argparse
import datetime

import collections
import inspect
import logging
import os.path
import time

import datetime
from ibapi import wrapper
from ibapi import utils
from ibapi.client import EClient
from ibapi.utils import iswrapper

from ContractSamples import ContractSamples

from ibapi.ticktype import TickType, TickTypeEnum
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# types
from ibapi.common import *  # @UnusedWildImport
from ibapi.order import *  # @UnusedWildImport
from DBHelperMay import DBHelper


def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)


def printWhenExecuting(fn):
    def fn2(self):
        print("   doing", fn.__name__)
        fn(self)
        print("   done w/", fn.__name__)

    return fn2

def printinstance(inst:Object):
    attrs = vars(inst)
    print(', '.join("%s: %s" % item for item in attrs.items()))

class Activity(Object):
    def __init__(self, reqMsgId, ansMsgId, ansEndMsgId, reqId):
        self.reqMsdId = reqMsgId
        self.ansMsgId = ansMsgId
        self.ansEndMsgId = ansEndMsgId
        self.reqId = reqId


class RequestMgr(Object):
    def __init__(self):
        # I will keep this simple even if slower for now: only one list of
        # requests finding will be done by linear search
        self.requests = []

    def addReq(self, req):
        self.requests.append(req)

    def receivedMsg(self, msg):
        pass

# ! [socket_init]
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




    # def dumpReqAnsErrSituation(self):
    #     logging.debug("%s\t%s\t%s\t%s" % ("ReqId", "#Req", "#Ans", "#Err"))
    #     for reqId in sorted(self.reqId2nReq.keys()):
    #         nReq = self.reqId2nReq.get(reqId, 0)
    #         nAns = self.reqId2nAns.get(reqId, 0)
    #         nErr = self.reqId2nErr.get(reqId, 0)
    #         logging.debug("%d\t%d\t%s\t%d" % (reqId, nReq, nAns, nErr))

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
            # self.historicalTicksOperations()
            # self.reqGlobalCancel()
            # self.marketDataTypeOperations()
            # self.accountOperations_req()
            # self.tickDataOperations_req()
            # self.marketDepthOperations_req()
            # self.realTimeBarsOperations_req()
            self.historicalDataOperations_req()
            # self.optionsOperations_req()
            # self.marketScannersOperations_req()
            # self.fundamentalsOperations_req()
            # self.bulletinsOperations_req()
            # self.contractOperations()
            # self.newsOperations_req()
            # self.miscelaneousOperations()
            # self.linkingOperations()
            # self.financialAdvisorOperations()
            # self.orderOperations_req()
            # self.rerouteCFDOperations()
            # self.marketRuleOperations()
            # self.pnlOperations_req()
            # self.histogramOperations_req()
            # self.continuousFuturesOperations_req()
            # self.historicalTicksOperations()
            # self.tickByTickOperations_req()
            # self.whatIfOrderOperations()
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
        # self.orderOperations_cancel()
        # self.accountOperations_cancel()
        # self.tickDataOperations_cancel()
        # self.marketDepthOperations_cancel()
        # self.realTimeBarsOperations_cancel()
        self.historicalDataOperations_cancel()
        # self.optionsOperations_cancel()
        # self.marketScanners_cancel()
        # self.fundamentalsOperations_cancel()
        # self.bulletinsOperations_cancel()
        # self.newsOperations_cancel()
        # self.pnlOperations_cancel()
        # self.histogramOperations_cancel()
        # self.continuousFuturesOperations_cancel()
        # self.tickByTickOperations_cancel()
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

    @printWhenExecuting
    def tickByTickOperations_req(self):
        # Requesting tick-by-tick data (only refresh)
        # ! [reqtickbytick]
        self.reqTickByTickData(19001, ContractSamples.EuropeanStock2(), "Last", 0, True)
        self.reqTickByTickData(19002, ContractSamples.EuropeanStock2(), "AllLast", 0, False)
        self.reqTickByTickData(19003, ContractSamples.EuropeanStock2(), "BidAsk", 0, True)
        self.reqTickByTickData(19004, ContractSamples.EurGbpFx(), "MidPoint", 0, False)
        # ! [reqtickbytick]

        # Requesting tick-by-tick data (refresh + historicalticks)
        # ! [reqtickbytickwithhist]
        self.reqTickByTickData(19005, ContractSamples.SimpleFuture(), "Last", 10, False)
        self.reqTickByTickData(19006, ContractSamples.SimpleFuture(), "AllLast", 10, False)
        self.reqTickByTickData(19007, ContractSamples.SimpleFuture(), "BidAsk", 10, False)
        self.reqTickByTickData(19008, ContractSamples.SimpleFuture(), "MidPoint", 10, True)
        # ! [reqtickbytickwithhist]

    @printWhenExecuting
    def historicalDataOperations_req(self, num_days = "5 D"):
        self.num_days = num_days
        # Requesting historical data
        # ! [reqHeadTimeStamp]
        # self.reqHeadTimeStamp(4101, ContractSamples.USStockAtSmart(), "TRADES", 0, 1)
        # ! [reqHeadTimeStamp]

        # ! [reqhistoricaldata]
        # this is where it ends
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=6)).strftime("%Y%m%d %H:%M:%S")
        # self.reqHistoricalData(4102, ContractSamples.SimpleFuture(), queryTime,
        #                        "1 M", "1 day", "MIDPOINT", 1, 1, False, [])
        # this is number of days back
        self.reqHistoricalData(4103, ContractSamples.SimpleFuture(), queryTime,
                               self.num_days, "1 day", "TRADES", 1, 1, False, [])




        # self.reqHistoricalData(4104, ContractSamples.SimpleFuture(), "",
        #                        "1 M", "1 day", "MIDPOINT", 1, 1, True, [])
        # ! [reqhistoricaldata]


    def historicalData(self, reqId: int, bar: BarData):
            print("HistoricalData. ReqId:", reqId, "BarData.", bar)


    # ! [historicaldata]


    @printWhenExecuting
    def historicalDataOperations_cancel(self):
        # ! [cancelHeadTimestamp]
        # self.cancelHeadTimeStamp(4101)
        # ! [cancelHeadTimestamp]
        # ! [cancelHeadTimestamp]

        # Canceling historical data requests
        # ! [cancelhistoricaldata]
        # self.cancelHistoricalData(4102)
        self.cancelHistoricalData(4103)
        # self.cancelHistoricalData(4104)
        # ! [cancelhistoricaldata]

    @iswrapper
    # ! [historicaldataend]
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)

    # ! [historicaldataend]

    @iswrapper
    # ! [historicalDataUpdate]
    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)

    # ! [historicalDataUpdate]

    def historicalData(self, reqId:int, bar: BarData):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        logging.debug("ReqId:", reqId, "BarData.", bar)
        # self.disconnect()


    @iswrapper
    def tickPrice(self, tickerId: TickerId , tickType: TickType, price: float, attrib):
        super().tickPrice(tickerId, tickType, price, attrib)
        print("Tick Price, Ticker Id:", tickerId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, " Time:", attrib.time, file=sys.stderr, end= " ")

    @iswrapper
    def tickSize(self, tickerId: TickerId, tickType: TickType, size: int):
        super().tickSize(tickerId, tickType, size)
        print( "Tick Size, Ticker Id:",tickerId,  "tickType:", TickTypeEnum.to_str(tickType),  "Size:", size, file=sys.stderr)

    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast, exchange: str,
                          specialConditions: str):
        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAttribLast,
                                  exchange, specialConditions)
        if tickType == 1:
            print("Last.", end='')
        else:
            print("AllLast.", end='')
        print(" ReqId:", reqId,
              "Time:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"),
              "Price:", price, "Size:", size, "Exch:", exchange,
              "Spec Cond:", specialConditions, "PastLimit:", tickAttribLast.pastLimit, "Unreported:",
              tickAttribLast.unreported)
        self.persistData(reqId, time, price,
                         size, tickAttribLast)

    def persistData(self, reqId: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast):
        #print(" inside persistData")
        contract = ContractSamples.SimpleFuture()
        values = (1,contract.symbol, reqId, time, price, size)
        db = DBHelper()
        db.insertData(values)

app = TestApp()
app.connect("127.0.0.1", 7497, clientId=3)
print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                              app.twsConnectionTime()))
app.run()

