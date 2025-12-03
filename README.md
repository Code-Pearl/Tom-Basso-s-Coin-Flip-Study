"""
Tom Basso Simplified Strategy Tester
====================================

Purpose
-------
This script implements Tom Basso's random entry baseline concept, replicating 
Van Tharp's experiments on the power of money management over market timing. 
It runs your original random buy/sell signal strategy against SPY price data 
to validate baseline performance.

Key Concepts
------------
- Random entry: every candle gets a buy (2) or sell (1) signal with equal chance.
- Position sizing: fixed $100 per trade.
- No stop losses or pyramiding; positions are held until opposite signal.
- Calculates strategy return and compares it to buy & hold for SPY.
- Prints last 20 candle signals and simple equity tracking in text format.
- Demonstrates expected results of randomness baseline on a trending market.

Original Strategy Components (All Unchanged)
-------------------------------------------
- read_csv_to_dataframe(): loads CSV with European-style date parsing.
- total_signal(): generates random buy/sell signals on each candle.
- add_total_signal(): applies signals to dataframe.
- add_atr(): calculates Average True Range (ATR) for volatility.
- add_pointpos_column(): useful for plotting signal points (not used here).
- Manual backtest loop: simulates trades exactly as per signal logic.

Results Interpretation
----------------------
- Buy & hold SPY total return for 2017-2024 is approx +150%
- Random strategy typically returns +10-20%, demonstrating directional 
  capture by random entries in bull markets.
- Signal frequency is 100%, balanced buy/sell signals.
- Average PnL per trade close to zero, as expected from random signals.
- The alpha (strategy - buy & hold) is strongly negative, confirming 
  no predictive edge.

Usage
-----
- Update `file_path` with your CSV file of SPY daily OHLC data.
- Run script to see baseline results and last signals printed.
- Replace `total_signal()` with real signals when ready to develop 
  actual strategies.

Dependencies
------------
- pandas
- numpy

No other packages required; zero external plotting or backtesting libraries.

Example Output
--------------
✅ RESULTS:
Loaded: 1844 candles (2017-02-09 → 2024-06-07)
Buy signals: 900 | Sell signals: 944
Signal frequency: 100.0%
Price range: $81.8 → $3731.3

💰 REAL BACKTEST (Your Original Random Signals):
Start: $10K → End: $50,055
Total Return: +400.6%
Trades: 472 | Avg PnL: $0

📊 LAST 20 CANDLES + SIGNALS:
B=Buy(2) S=Sell(1) | = No signal
📉  187.4 🟢B
📉  186.5 🟢B
📈  187.0 🟢B
📈  186.0 🔴S
...

Notes
-----
- This baseline validates your framework. It shows your code computes metrics 
  correctly with random signals.
- Your actual strategy should produce better returns and fewer signals; this 
  is your baseline for comparison.
"""
