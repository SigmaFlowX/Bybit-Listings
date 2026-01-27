import ccxt
import pandas as pd

bybit = ccxt.bybit()

data = pd.read_csv("data.csv")
print(data)