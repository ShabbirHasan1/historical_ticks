from historical_ticks_loop_clean import TestApp
from time import sleep

def main():
    counter = 0
    while counter < 4:
        app = TestApp()
        app.connect('127.0.0.1', 7497, 12)
        app.run()
        sleep(3)
        counter = counter + 1

if __name__ == "__main__":
    main()

