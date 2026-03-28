import pandas as pd
from fredapi import Fred
import statsmodels.api as sm

fred = Fred(api_key="YOUR_FRED_API_KEY_HERE")
start_date = "2016-03-01"  # Fixed start date (sp500 data only goes back 10 years)

# Get data
cpi = fred.get_series("CPIAUCSL", observation_start=start_date)
gdp = fred.get_series("GDP", observation_start=start_date)
real_rate = fred.get_series("REAINTRATREARAT10Y", observation_start=start_date)
sent = fred.get_series("UMCSENT", observation_start=start_date)
unemployment = fred.get_series("UNRATE", observation_start=start_date)
sp500_daily_values = fred.get_series("SP500", observation_start=start_date)

# Resample GDP to monthly and compute monthly growth rate
gdp_m = gdp.resample('MS').asfreq().interpolate(method='linear').pct_change(1)

# Fill in missing monthly information and compute monthly growth rates
inflation_m = cpi.interpolate(method='linear').pct_change(1)
sent_m = sent.interpolate(method='linear').pct_change(1)
real_m = real_rate.interpolate(method='linear').diff(1)  # Take first difference
unemployment_m = unemployment.ffill().interpolate(method='linear').diff(1)  # Take first difference

# Compute monthly S&P 500 returns with 5-day rolling average
sp500_ret_daily = sp500_daily_values.pct_change(1)
sp500_ret_monthly = sp500_ret_daily.rolling(window=5, center=True).mean().resample('MS').last()

# Create DataFrame
df = pd.DataFrame({
    'inflation': inflation_m,
    'GDP': gdp_m,
    'SENT': sent_m,
    'REAL_RATE': real_m,
    'UNEMPLOYMENT': unemployment_m,
    'spx_ret': sp500_ret_monthly
})

indicators = ['GDP', 'UNEMPLOYMENT', 'REAL_RATE', 'SENT']

# Shift indicators (predict sp500_t using economic indicator_t-1)
df[indicators] = df[indicators].shift(1)

# Shift Real Rate an additional 2 months (total lag of 3 months)
df['REAL_RATE'] = df['REAL_RATE'].shift(2)

# Drop missing values
df = df.dropna()

# Fit OLS regression model
Y = df["spx_ret"]
X = df[indicators]
X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()
print(model.summary())