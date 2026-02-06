# About the idea 
A long time ago I noticed that listings on large cryptoexchangs are significant events for cryptocoins. <br>
They seem to experience major moves in upcoming weeks: they can go down as hype around them peaks and then vanishes or go up as hype continues its climb. <br>
Therefore, I have decided to gather some data from free public apis and see what I can do with that.
# About the obtained data

**step 1:** Vibe-coded parser gets tickers of latest listed coins from the official bybit announcements api. 

**step2:** Two features are added to data using results of step1: asset type (spot or contract) and listing order (sometimes contracts are listed first, sometime spots). 

**step3:** Using ccxt library following post-listing-perforamce is gathered:<br> 
1. one hour, one week and one month returns after listing
2. whether asset was delisted or not
3. exact listing time is also obtained (parser may get it wrong)

**step4:** Using coingecko api following pre-listing-data is obtained:
1. market cap one day before listing
2. price changes one week and one day before listing
3. volume changes onew week and one day before listing

# Results
final dataset looks like followng:
| ticker         | base_coin   | listing_time        |   asset_type |   listing_order | accurate_listing_time     |   one_hour_post_listing_performance |   one_day_post_listing_performance |   one_month_post_listing_performance |   is_delisted | coingecko_id    |   marketcap_minus1d |   price_change_minus1d |   price_change_minus7d |   volume_change_minus1d |   volume_change_minus7d |
|:---------------|:------------|:--------------------|-------------:|----------------:|:--------------------------|------------------------------------:|-----------------------------------:|-------------------------------------:|--------------:|:----------------|--------------------:|-----------------------:|-----------------------:|------------------------:|------------------------:|
| WHITEWHALEUSDT | WHITEWHALE  | 2026-01-06 12:27:10 |            1 |               2 | 2026-01-06 12:27:00+00:00 |                                 2.5 |                               -2.5 |                                 24.7 |             0 | the-white-whale |         8.45754e+07 |               18.2168  |              38.5024   |                 11.0818 |                -2.37413 |
| WHITEWHALE     | WHITEWHALE  | 2026-01-06 07:28:20 |            0 |               2 | 2026-01-06 12:00:00+00:00 |                                -4.2 |                               -8.6 |                                 17.3 |             0 | the-white-whale |         8.45754e+07 |               18.2168  |              38.5024   |                 11.0818 |                -2.37413 |
| POWERUSDT      | POWER       | 2025-12-29 10:46:00 |            1 |               1 | 2025-12-29 10:45:00+00:00 |                                 2.2 |                                7.6 |                                -40.2 |             0 | power-protocol  |         6.90768e+07 |               -1.07598 |               9.84667  |                -57.6557 |               -29.9331  |
| MAGMAUSDT      | MAGMA       | 2025-12-26 07:40:00 |            1 |               1 | 2025-12-26 07:40:00+00:00 |                                 3.8 |                               10.6 |                                -29.7 |             0 | magma-finance   |         2.47955e+07 |              -16.394   |              -0.820748 |                -14.982  |                43.7087  |
| USUSDT         | US          | 2025-12-12 11:21:10 |            1 |               2 | 2025-12-12 11:21:00+00:00 |                                -8.6 |                              -28.8 |                                -71.3 |             0 | ultrasolid      |    372547           |               -2.5769  |             -14.2607   |                 11.2208 |                10.918   |


Unfortunately, I managed to get full data for only around 130 coins. <br>
That is way too low to build an ML model. <br>
Moreover, the data is heavily biased towards a negative side as apprx. 80% of coins fell in the following month after listing.
