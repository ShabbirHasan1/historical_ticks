from historical_ticks_loop_clean import TestApp

app = TestApp()
app.connect('127.0.0.1', 7497, 12)
app.run()
