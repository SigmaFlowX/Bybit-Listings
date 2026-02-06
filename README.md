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
