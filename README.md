# Stock Signal Analyzer

A Python tool that analyzes stock price trends using technical indicators and generates BUY/SELL/HOLD signals based on your portfolio. Built as a learning project for AI & Data Science coursework.

## What it does

- Takes a company name (e.g. "Apple", "HDFC Bank") and automatically finds the correct stock ticker
- Fetches 2 years of historical price data
- Calculates two technical indicators: SMA (Simple Moving Average) and RSI (Relative Strength Index)
- Generates a BUY, SELL, or HOLD signal based on a combination of both indicators
- Calculates your personal profit/loss based on shares owned and purchase price
- Backtests the signal strategy against a simple buy-and-hold approach over the same period

## How the signal works

- **BUY** when the 20-day average price is above the 50-day average (uptrend) and RSI is below 70 (not overbought)
- **SELL** when the 20-day average is below the 50-day average (downtrend) and RSI is above 30 (not oversold)
- **HOLD** otherwise

## Backtest results

Tested against 3 stocks, comparing the strategy's performance to simply buying and holding:

| Ticker | Strategy Return | Buy & Hold Return | Strategy Won? |
|---|---|---|---|
| HDB | +1.41% | -22.90% | Yes |
| AAPL | +16.07% | +47.93% | No |
| INFY.NS | -20.73% | -42.27% | Yes |

**Finding:** the strategy tends to reduce losses during downtrends by moving to cash, but sacrifices some gains during strong sustained uptrends by trading in and out rather than holding continuously.




## Backtest results

Tested against 4 stocks, comparing the rule-based strategy's performance to simply buying and holding, plus a Random Forest ML model's accuracy at predicting next-day price direction:

| Ticker | Strategy Return | Buy & Hold Return | Strategy Won? | ML Accuracy |
|---|---|---|---|---|
| HDB | +1.41% | -22.90% | Yes | 45.05% |
| AAPL | +16.07% | +47.93% | No | 49.45% |
| INFY.NS | -20.73% | -42.27% | Yes | — |
| ONGC.NS | -12.96% | -7.54% | No | 43.33% |

**Findings:**
- The rule-based strategy's performance relative to buy-and-hold was mixed (2 wins, 2 losses out of 4) — no consistent pattern by trend direction emerged, contrary to an early hypothesis that it would reliably reduce losses during downtrends.
- The Random Forest model's accuracy (43-49%) was consistently at or below the 50% baseline expected from random guessing across all tests. This is consistent with the efficient market hypothesis — daily price direction is difficult to predict from technical indicators alone, especially with a limited ~2-year dataset.
- Overall, neither approach reliably "beats the market," which is expected and consistent with real-world quantitative finance research. The value of this project is in building and honestly evaluating these approaches, not in achieving high predictive accuracy.





## Limitations

- This is a decision-support tool, not a prediction system — no model can reliably predict short-term stock price movement, and this project should not be used as financial advice
- The company name search relies on an unofficial API endpoint and can occasionally fail to find the correct regional listing (e.g. searching "HDFC" alone sometimes returns a US-listed ADR instead of the Indian NSE listing) — searching with the fuller company name or entering the exact ticker helps
- Backtesting was done on a small sample of stocks over one time period; results may not generalize to all market conditions

## How to run it

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python FetchData.py`
4. Follow the prompts to enter a company name, country, share quantity, and buy price

## Tech used

- Python
- yfinance (stock data)
- pandas (data handling)
- matplotlib (charting)
- requests (ticker lookup API)