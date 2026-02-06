import pandas as pd
import requests
from datetime import datetime, timedelta
import time
pd.set_option("display.max_rows", 20)
pd.set_option("display.width", 1000)
pd.set_option("display.expand_frame_repr", False)


data = pd.read_csv("../listing+post_data.csv")

#add coingecko-id for each ticker
url = "https://api.coingecko.com/api/v3/coins/list"
r = requests.get(url, timeout=20)
r.raise_for_status()
coins = r.json()
symbol_to_id = {coin['symbol'].lower(): coin['id'] for coin in coins}
data['coingecko_id'] = data['base_coin'].str.lower().map(symbol_to_id)




data['marketcap_minus1d'] = None
data['price_change_minus1d'] = None
data['price_change_minus7d'] = None
data['volume_change_minus1d'] = None
data['volume_change_minus7d'] = None

for i in data.index:
    token_id = data['coingecko_id'][i]
    if pd.isna(token_id): continue

    if not pd.isna(data['accurate_listing_time'][i]):
        listing_date = data['accurate_listing_time'][i]
    else:
        listing_date = data['listing_time'][i]


    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart/range"
    from_date = pd.to_datetime(listing_date) - pd.Timedelta(days=7)
    params = {
        "vs_currency": "usd",
        "from": from_date.date(),
        "to": pd.to_datetime(listing_date).date(),
        "x_cg_demo_api_key": "CG-Qz4b9yrLigchwdX3dcgHMp8Q",
    }

    while True:
        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            inf = r.json()
            break
        except requests.exceptions.HTTPError as e:
            if r.status_code == 401:
                print(f"401 for token {token_id} \n Probably out of 1 year range (coingecko limit). Further search is useless, you can stop now")
                break
        except Exception as e:
            print("Unexpected error in request, sleeping")
            time.sleep(60)

    if not inf.get("prices"):
        print(f"Empty data for token {token_id}")
        continue

    df_prices = pd.DataFrame(inf["prices"], columns=["timestamp", "price"])
    df_mc = pd.DataFrame(inf["market_caps"], columns=["timestamp", "market_cap"])
    df_vol = pd.DataFrame(inf["total_volumes"], columns=["timestamp", "volume"])
    df = (
        df_prices
        .merge(df_mc, on="timestamp", how="left")
        .merge(df_vol, on="timestamp", how="left")
    )
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("date")
    #coingecko give either daily or hourly data
    deltas = df.index.sort_values().diff().dropna()
    if deltas[0] < pd.Timedelta(hours=23):
        df = df.resample("1D").agg({
            "price": "last",
            "market_cap": "last",
            "volume": "sum"
        }).reset_index()


    if len(df) >= 2:
        market_cap_minus1d = df['market_cap'].iloc[-1]
        price_change_minus1d = (df['price'].iloc[-1] - df['price'].iloc[-2])/df['price'].iloc[-2] * 100
        volume_change_minus1d = (df['volume'].iloc[-1] - df['volume'].iloc[-2]) / df['volume'].iloc[-2] * 100

        data.at[i, 'marketcap_minus1d'] = market_cap_minus1d
        data.at[i, 'price_change_minus1d'] = price_change_minus1d
        data.at[i, 'volume_change_minus1d'] = volume_change_minus1d
    if len(df) >= 7:
        price_change_minus7d = (df['price'].iloc[-1] - df['price'].iloc[-7]) / df['price'].iloc[-7] * 100
        volume_change_minus7d = (df['volume'].iloc[-1] - df['volume'].iloc[-7]) / df['volume'].iloc[-7] * 100

        data.at[i, 'price_change_minus7d'] = price_change_minus7d
        data.at[i, 'volume_change_minus7d'] = volume_change_minus7d

    data.to_csv("listing+post+pre_data.csv", index=False)
    print(f"Done for token {token_id}")
    print(i)
    time.sleep(2)