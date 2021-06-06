from historical_ticks_loop_clean import TestApp
import pandas as pd
import time

def main():
    counter = 0
    while counter < 2:
        app = TestApp()
        app.connect('127.0.0.1', 7497, 12)
        app.run()
        data_list = []
        data_list.append(app.data)
        time.sleep(2)
        df3 = pd.DataFrame(app.data)
        counter = counter + 1
        df3.to_csv('appended.csv')


if __name__ == "__main__":
    main()

