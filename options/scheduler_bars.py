import schedule
from historical_options_bars_clean import TestApp

def job():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=3)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                  app.twsConnectionTime()))
    app.run()
    app.disconnect()


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
