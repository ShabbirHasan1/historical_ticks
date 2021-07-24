import schedule
import historical_bars_five_mins

def job():
    print('Hello World')


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
