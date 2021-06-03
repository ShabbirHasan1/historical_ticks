import time
import datetime

queryTime = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime("%Y%m%d %H:%M:%S")
print(queryTime)