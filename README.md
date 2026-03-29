# S&P 500 Return Prediction Model
## Overview
A regression model predicting S&P 500 monthly returns using macroeconomic indicators from the Federal Reserve Economic Data (FRED) API.
## Results
- **R² = 0.133** (explains 13.3% of monthly return variation)
- **F-statistic = 4.14** with **p = 0.0037** (model is statistically significant)
- **Sample:** 113 monthly observations (2016-2026)
## Model Specification

S&P 500 Return = β₀ + β₁(GDP) + β₂(Unemployment) + β₃(Real Rate) + β₄(Sentiment) + ε

## Key Findings
| Variable | Coefficient | P-value | Interpretation |
|----------|-------------|---------|-----------------|
| GDP Growth | 0.192 | 0.001 | Economic expansion drives returns |
| Unemployment Change | 0.0012 | 0.003 | Rising unemployment associated with higher returns |
| Real Interest Rate Change | 0.0034 | 0.028 | Higher real rates associated with higher returns |
| Consumer Sentiment Growth | 0.0086 | 0.147 | Higher consumer sentiment associated with higher returns |
## Data Source
Federal Reserve Economic Data (FRED) API - https://fredaccount.stlouisfed.org/
## Usage
1. Get a free FRED API key from https://fredaccount.stlouisfed.org/login
2. Replace YOUR_FRED_API_KEY_HERE with your actual key
3. Run:
bash
pip install pandas fredapi statsmodels
python "S&P 500 Prediction Model.py"

## Methodology
- **Data Source:** FRED API (monthly, 2016-2026)
- **Features:** GDP growth, unemployment change, real interest rates (10Y), consumer sentiment
- **Transformations:** Linear interpolation, percentage change, first differencing
- **Model:** Ordinary Least Squares (OLS) regression
- **Time Lags:** Most indicators lagged 1 month; real rates lagged 3 months
## Limitations
- Small sample size (113 observations ~ 10 years of data)
- Assumes linear relationships
- Does not account for structural breaks or regime changes
- Stock returns are inherently noisy
## Files
- S&P 500 Prediction Model.py - Main model code
- README.md - This file
