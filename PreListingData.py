import pandas as pd
import requests
from datetime import datetime, timedelta
import time



# data = pd.read_csv("listing+market_data.csv")
#
# #add coingecko-id for each ticker
# url = "https://api.coingecko.com/api/v3/coins/list"
# r = requests.get(url, timeout=20)
# r.raise_for_status()
# coins = r.json()
# symbol_to_id = {coin['symbol'].lower(): coin['id'] for coin in coins}
# data['coingecko_id'] = data['base_coin'].str.lower().map(symbol_to_id)


#getting prelisting marketcap data
data = pd.read_csv("listing+market+prelisting_data.csv")
#data['market_cap_minus1d'] = None
for i in range(550, 650):
    token = data['base_coin'][i]
    token_id = data['coingecko_id'][i]
    if pd.isna(data['coingecko_id'][i]):continue
    if not pd.isna(data['accurate_listing_time'][i]):
        listing_date = data['accurate_listing_time'][i]
    else:
        listing_date = data['listing_time'][i]



    # taking -1 day to ensure no look-ahead bias
    listing_date = dt = datetime.fromisoformat(listing_date)
    listing_date = listing_date.date()
    listing_date_minus1 = listing_date - timedelta(days=1)

    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/history"
    params = {
        "date": listing_date_minus1,
        "localization": "false",
        "x_cg_demo_api_key": "CG-Qz4b9yrLigchwdX3dcgHMp8Q"
    }

    while True:
        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            inf = r.json()
            market_cap = inf.get("market_data", {}).get("market_cap", {}).get('usd')
            if market_cap is None or market_cap == 0.0:
                time.sleep(3)
                params = {
                    "date": listing_date,
                    "localization": "false",
                    "x_cg_demo_api_key": "CG-Qz4b9yrLigchwdX3dcgHMp8Q"
                }
                r = requests.get(url, params=params)
                r.raise_for_status()
                inf = r.json()
                market_cap = inf.get("market_data", {}).get("market_cap", {}).get('usd')


            data.at[i, 'market_cap_minus1d'] = market_cap
            data.to_csv("listing+market+prelisting_data.csv", index=False)
            break
        except requests.exceptions.HTTPError as e:
            if r.status_code == 401:
                print("asdasd")
                market_cap = None
                break
        except Exception as e:
            print(e)
            time.sleep(60)

    print(i)
    print(token, market_cap)
    time.sleep(2)




