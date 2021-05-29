import csv
import argparse
import datetime

import collections
import inspect
import logging
import os.path
import time


import pandas as pd
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

    def dumpReqAnsErrSituation(self):
        logging.debug("%s\t%s\t%s\t%s" % ("ReqId", "#Req", "#Ans", "#Err"))
        for reqId in sorted(self.reqId2nReq.keys()):
            nReq = self.reqId2nReq.get(reqId, 0)
            nAns = self.reqId2nAns.get(reqId, 0)
            nErr = self.reqId2nErr.get(reqId, 0)
            logging.debug("%d\t%d\t%s\t%d" % (reqId, nReq, nAns, nErr))

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
            self.historicalTicksOperations()

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
        # self.historicalDataOperations_cancel()
        # self.optionsOperations_cancel()
        # self.marketScanners_cancel()
        # self.fundamentalsOperations_cancel()
        # self.bulletinsOperations_cancel()
        # self.newsOperations_cancel()
        # self.pnlOperations_cancel()
        # self.histogramOperations_cancel()
        # self.continuousFuturesOperations_cancel()
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
    def historicalTicksOperations(self):
        # ! [reqhistoricalticks]
        self.reqHistoricalTicks(18001, ContractSamples.SimpleFuture(),
                                "20210526 09:39:33", "", 1000, "TRADES", 1, True, [])
        # self.reqHistoricalTicks(18002, ContractSamples.SimpleFuture(),
        #                         "20210525 09:39:33", "", 10, "BID_ASK", 1, True, [])
        # self.reqHistoricalTicks(18003, ContractSamples.SimpleFuture(),
        #                         "20210525 09:39:33", "", 10, "MIDPOINT", 1, True, [])
        # ! [reqhistoricalticks]


    @printWhenExecuting
    def tickDataOperations_req(self):
        self.reqMarketDataType(MarketDataTypeEnum.DELAYED_FROZEN)

        #self.reqMktData(1015, ContractSamples.SimpleFuture(), "", False, False, [])
        #self.reqMktData(1999, ContractSamples.USSPYStockAtSmart(), "233,236,258", False, False, [])
        #self.reqHistoricalData(2, ContractSamples.ContFut(), "", "1 Y", "1 hour", "BID_ASK", 0, 1, False, []);
        self.reqTickByTickData(19002, ContractSamples.SimpleFuture(), "AllLast", 0, False)

    @iswrapper
    # ! [historicalticks]
    def historicalTicks(self, reqId: int, ticks: ListOfHistoricalTick, done: bool):
        for tick in ticks:
            print("HistoricalTick. ReqId:", reqId, tick)

    # ! [historicalticks]

    @iswrapper
    # ! [historicalticksbidask]
    def historicalTicksBidAsk(self, reqId: int, ticks: ListOfHistoricalTickBidAsk,
                              done: bool):
        for tick in ticks:
            print("HistoricalTickBidAsk. ReqId:", reqId, tick)

    # ! [historicalticksbidask]

    @iswrapper
    # ! [historicaltickslast]
    def historicalTicksLast(self, reqId: int, ticks: ListOfHistoricalTickLast,
                            done: bool):
        for tick in ticks:
            print("HistoricalTickLast. ReqId:", reqId, tick)

    # ! [historicaltickslast]

    def historicalData(self, reqId:int, bar: BarData):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
        logging.debug("ReqId:", reqId, "BarData.", bar)


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


def main():
    SetupLogger()
    logging.getLogger().setLevel(logging.ERROR)

    cmdLineParser = argparse.ArgumentParser("api tests")
    # cmdLineParser.add_option("-c", action="store_True", dest="use_cache", default = False, help = "use the cache")
    # cmdLineParser.add_option("-f", action="store", type="string", dest="file", default="", help="the input file")
    cmdLineParser.add_argument("-p", "--port", action="store", type=int,
                               dest="port", default=7497, help="The TCP port to use")
    cmdLineParser.add_argument("-C", "--global-cancel", action="store_true",
                               dest="global_cancel", default=False,
                               help="whether to trigger a globalCancel req")
    args = cmdLineParser.parse_args()
    print("Using args", args)
    logging.debug("Using args %s", args)
    # print(args)

    # tc = TestClient(None)
    # tc.reqMktData(1101, ContractSamples.USStockAtSmart(), "", False, None)
    # print(tc.reqId2nReq)
    # sys.exit(1)
    app = TestApp()
    try:
        if args.global_cancel:
            app.globalCancelOnly = True
        # ! [connect]
        app.connect("127.0.0.1", args.port, clientId=0)
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