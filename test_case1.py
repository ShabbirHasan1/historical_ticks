from historical_bars import TestApp
from historical_bars import SetupLogger

import logging
import argparse

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
