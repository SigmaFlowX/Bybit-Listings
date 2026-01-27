import ccxt
import pandas as pd

date_str = '2020-01-01'
since = int(pd.Timestamp(date_str).timestamp() * 1000)

bybit = ccxt.bybit()
data = pd.read_csv("listing_data.csv")

data['one_hour_post_listing_performance'] = None
data['one_day_post_listing_performance'] = None
data['one_month_post_listing_performance'] = None
data['is_delisted'] = 0

for i in data.index:
    if data['asset_type'][i] == 0: ticker = data['ticker'][i] + "/USDT"
    else: ticker = data['ticker'][i]

    try:
        m_ohlcv = bybit.fetch_ohlcv(ticker, timeframe="1m", since=since, limit=1)
        h_ohlcv = bybit.fetch_ohlcv(ticker, timeframe="1h", since=since, limit=1)
        d_ohlcv = bybit.fetch_ohlcv(ticker, timeframe="1d", since=since, limit=31)
    except:
        print("No data for", ticker)
        data.at[i, 'is_delisted'] = 1
        continue

    if m_ohlcv and h_ohlcv and d_ohlcv and len(d_ohlcv) == 31:
        base_price = m_ohlcv[0][4]
        one_hour_price = h_ohlcv[0][4]
        one_day_price = d_ohlcv[0][4]
        one_month_price = d_ohlcv[30][4]

        data.at[i, 'one_hour_post_listing_performance'] = round((one_hour_price - base_price) / base_price, 2)
        data.at[i, 'one_day_post_listing_performance'] = round((one_day_price - base_price) / base_price, 2)
        data.at[i, 'one_month_post_listing_performance'] = round ((one_month_price - base_price)/base_price, 2)
        print("found data for", ticker)
    else:
        print("Not enough data for", ticker)

data.to_csv("listing+market_data.csv", index=False)
print(data.head(5))