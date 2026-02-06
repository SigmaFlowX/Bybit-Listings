import pandas as pd

data = pd.read_csv("../bybit_listings.csv")

data['asset_type'] = data['ticker'].apply(lambda x: 1 if 'USDT' in x else 0)
data['base_coin'] = data['ticker'].apply(lambda x: x.replace('USDT', ''))
data['listing_time'] = pd.to_datetime(data['listing_time'])
data['listing_order'] = None

for coin, group in data.groupby('base_coin'):
    spot_row = group[group['asset_type'] == 0]
    contract_row = group[group['asset_type'] == 1]

    if not spot_row.empty and contract_row.empty:
        data.loc[group.index, 'listing_order'] = 0
    elif spot_row.empty and not contract_row.empty:
        data.loc[group.index, 'listing_order'] = 1
    else:
        spot_time = spot_row['listing_time'].values[0]
        contract_time = contract_row['listing_time'].values[0]
        if spot_time < contract_time:
            data.loc[group.index, 'listing_order'] = 2
        else:
            data.loc[group.index, 'listing_order'] = 3

data = data[['ticker', 'base_coin', 'listing_time' ,'asset_type', 'listing_order']]

data.to_csv("listing_data.csv", index=False)
