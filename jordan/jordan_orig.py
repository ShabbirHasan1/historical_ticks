
# You're script ran as designed.  I pulled over the following into my script:

import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from ibapi.utils import iswrapper
# import ta
import numpy as np
import pandas as pd
import pytz
import math
from datetime import datetime, timedelta
import threading
import time
import collections
from calcs_helper import calculate_ema, atr_num, rsi
from scipy.stats import norm
import datetime
from time import time, sleep

# Vars
orderId = 1
SLOW_PERIOD = 80
FAST_PERIOD = 6
position_ = 'out'


# Class for Interactive Brokers Connection
class IBApi(EWrapper, EClient):
    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.data = []  # Initialize variable to store candle
        self.df = pd.DataFrame()
        self.one_pct_rule = 0

    # Historical Backtest Data
    def historicalData(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, False)
        except Exception as e:
            print(e)

    # On Realtime Bar after historical data finishes
    def historicalDataUpdate(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, True)
        except Exception as e:
            print(e)

    # On Historical Data End
    def historicalDataEnd(self, reqId, start, end):
        print(reqId)

    def nextValidId(self, nextorderId):
        global orderId
        orderId = nextorderId

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
        # self.data.append([tag, value])
        self.df = pd.DataFrame(self.data, columns=['Account', 'Value'])
        # print(self.df)
        # self.df.to_csv('acct_value.csv')
        if len(self.df) == 24:
            net_liquid = self.df.loc[8, 'Value']
            self.one_pct_rule = .01 * float(net_liquid)
            # print(f'net liquidation value: {net_liquid}')
            # print(f'1% allocation:  {one_pct_rule}')

    def error(self, id, errorCode, errorMsg):
        print(errorCode)
        print(errorMsg)


# Bot Logic
class Bot:
    ib = None
    reqId = 1
    SLOW_PERIOD = 30
    FAST_PERIOD = 6
    global orderId
    initialbartime = datetime.datetime.now().astimezone(pytz.timezone("America/New_York"))

    def __init__(self):
        # Connect to IB on init
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        # self.accountSummary(req_id)
        self.low = collections.deque(maxlen=SLOW_PERIOD)
        self.high = collections.deque(maxlen=SLOW_PERIOD)
        self.close = collections.deque(maxlen=SLOW_PERIOD)
        self.long_ema = collections.deque(maxlen=SLOW_PERIOD)
        self.short_ema = collections.deque(maxlen=FAST_PERIOD)
        self.nmc = 0
        self.ib_api = IBApi()

        # Create our IB Contract Object
        contract = Contract()
        contract.symbol = "ES"
        contract.secType = "FUT"
        contract.exchange = "GLOBEX"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "202109"
        self.ib.reqIds(-1)

        self.ib.reqHistoricalData(self.reqId, contract, "", "5 D", "5 mins", "TRADES", 0, 1, True, [])
        # self.ib.reqPositions(self.reqId)
        # print(self.pos)
        # Listen to socket in seperate thread


    def run_loop(self):
        self.ib.run()

    # Bracet Order Setup
    def bracketOrder(self, parentOrderId, action, quantity, profitTarget, stopLoss):
        # Initial Entry
        # Create Parent Order / Initial Entry
        parent = Order()
        parent.orderId = parentOrderId
        parent.orderType = "MKT"
        parent.action = action
        parent.totalQuantity = quantity
        parent.transmit = False
        # Profit Target
        profitTargetOrder = Order()
        profitTargetOrder.orderId = parent.orderId + 1
        profitTargetOrder.orderType = "LMT"
        profitTargetOrder.action = "SELL" if action == "BUY" else "BUY"
        profitTargetOrder.totalQuantity = quantity
        profitTargetOrder.lmtPrice = profitTarget
        profitTargetOrder.parentId = parentOrderId
        profitTargetOrder.transmit = False
        # Stop Loss
        stopLossOrder = Order()
        stopLossOrder.orderId = parent.orderId + 2
        stopLossOrder.orderType = "STP"
        stopLossOrder.action = "SELL" if action == "BUY" else "BUY"
        stopLossOrder.totalQuantity = quantity
        stopLossOrder.parentId = parentOrderId
        stopLossOrder.auxPrice = stopLoss
        stopLossOrder.transmit = True

        bracketOrders = [parent, profitTargetOrder, stopLossOrder]

        return bracketOrders

    # Pass realtime bar data back to our bot object
    def on_bar_update(self, reqId, bar, realtime):
        global orderId
        global position_
        # if self.pos > 0:
        #     print("{} Position/s on in {}.".format(self.pos, contract.symbol))
        # else:
        # append values
        self.low.append(bar.close)
        self.high.append(bar.high)
        self.close.append(bar.close)
        self.long_ema.append(bar.close)
        self.short_ema.append(bar.close)

        # check time for market hours (regular)
        now = datetime.datetime.now()
        if (now.time() < datetime.time(1, 30) or now.time() > datetime.time(16, 00)):
            print("Regular Market Hours Not Open")
        else:
            # Calculate EWA
            if len(self.long_ema) == SLOW_PERIOD:
                ema_15 = np.array(self.long_ema)
                ema_6 = np.array(self.short_ema)
                low_ = np.array(self.low)
                high_ = np.array(self.high)
                close_ = np.array(self.close)

                fast_avg = calculate_ema(ema_6, 6)[-1]
                slow_avg = calculate_ema(ema_15[-6:], 15)[-1]

                # Calculate ATR
                atr = atr_num(h=high_, l=low_,
                              c=close_, window=15)

                # Compute MACD and the signal line if the MACD list is full
                num = fast_avg - slow_avg
                denom = (atr * np.sqrt((.5 * (15 - 1) + 7) - (.5 * (7 - 1))))
                norm_diff = num / denom
                self.nmc = (1 * norm_diff) - 50

                rsi2 = rsi(close_, window=15)[-2:-1]
                rsi40 = rsi(close_, window=15)[-40:-39]
                # x_rsi = np.column_stack((rsi40, premarket))
                preds_rsi = (rsi40 * 0.223)  # +(premarket*1.1865)
                self.diff_rsi = preds_rsi - rsi2

                self.preds = (self.diff_rsi * 4.977e-05) + (self.nmc * 3.785e-05)

                print("Prediction : {}. Position is {}".format(self.preds, position_))

                # Check Criteria
                if (self.preds >= -0.003450411116078039124
                ) and (position_ == 'out'):
                    # Bracket Order 4% Profit Target 1% Stop Loss
                    profitTarget_ = round(((bar.close * 1.04) * 4) / 4)
                    stopLoss_ = round(((bar.close * .99) * 4) / 4)
                    quantity_ = np.floor(one_pct_rule / bar.close)
                    bracket = self.bracketOrder(orderId,
                                                action="BUY", quantity=quantity_,
                                                profitTarget=profitTarget_,
                                                stopLoss=stopLoss_)
                    contract = Contract()
                    contract.symbol = "ES"
                    contract.secType = "FUT"
                    contract.exchange = "GLOBEX"
                    contract.currency = "USD"
                    contract.lastTradeDateOrContractMonth = "202109"

                    # Place Bracket Order
                    for o in bracket:
                        # o.ocaGroup = "OCA_"+str(orderId)
                        self.ib.placeOrder(o.orderId, contract, o)
                        print(o.orderId)
                        # self.nextorderId()
                    orderId += 3
                    position_ = "long"
                    print(position_, "Order placed on IDs", orderId)


                elif (self.preds <= -0.000987
                ) and position_ == 'out':
                    # Bracket Order 4% Profit Target 1% Stop Loss
                    profitTarget_ = round(((price * .96) * 4) / 4)
                    stopLoss_ = round((bar.close * 1.02) * 4) / 4
                    quantity_ = np.floor(self.ib_api.one_pct_rule / bar.close)
                    bracket_s = self.bracketOrder(orderId, action="SELL",
                                                  quantity=quantity_,
                                                  profitTarget=profitTarget_,
                                                  stopLoss=stopLoss_)
                    contract = Contract()
                    contract.symbol = "ES"
                    contract.secType = "FUT"
                    contract.exchange = "GLOBEX"
                    contract.currency = "USD"
                    contract.lastTradeDateOrContractMonth = "202109"

                    for o in bracket_s:
                        print(o.orderId)
                        self.ib.placeOrder(o.orderId, contract, o)
                        print(o.orderId)
                    orderId += 3
                    position_ = "Short"
                    print(position_, "Order placed on IDs", orderId)


# Start Bot
bot = Bot()


def run_loop(self):
    self.ib.run()

