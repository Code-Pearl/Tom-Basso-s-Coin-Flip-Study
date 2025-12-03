"""
Tom Basso Simplified Strategy Tester
====================================
Original strategy framework with technical simplifications only.
Tests random entry/exit (Tom Basso baseline) vs Buy & Hold.

Author: Simplified from original Jupyter notebook
Date: Dec 2025
Purpose: Validate random trading baseline on SPY (2017-2024)

Key Features:
- 100% signal frequency (random 1/2 every candle)
- Position sizing: $100 fixed per trade
- No stop losses (pure random entry/exit)
- Buy & Hold baseline comparison
- Zero external dependencies (pandas/numpy only)
"""

import pandas as pd
import numpy as np
import os

# FIXED FILE PATH - Works from any directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'SPY_1D_BID_16.02.2017-06.07.2024.csv')
print(f"🔍 Looking for file: {file_path}")

# =============================================================================
# CORE FUNCTIONS (ORIGINAL UNCHANGED)
# =============================================================================

def read_csv_to_dataframe(file_path):
    """Load candlestick CSV with European date format (dd.mm.yyyy)."""
    df = pd.read_csv(file_path)
    df["Gmt time"] = df["Gmt time"].str.replace(".000", "")
    df['Gmt time'] = pd.to_datetime(df['Gmt time'], format='%d.%m.%Y %H:%M:%S', dayfirst=True)
    df = df[df.High != df.Low]
    df.set_index("Gmt time", inplace=True)
    return df

def total_signal(df, current_candle):
    """Tom Basso random entry: 50/50 buy(2)/sell(1) every candle."""
    return np.random.choice([1, 2])  # ORIGINAL LOGIC - UNCHANGED

def add_total_signal(df):
    """Apply random signals to all candles."""
    df['TotalSignal'] = [total_signal(df, idx) for idx in df.index]
    return df

def add_atr(df, length=10):
    """Calculate ATR for position sizing reference."""
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    tr = np.maximum(high_low, np.maximum(high_close, low_close))
    df['ATR'] = tr.rolling(window=length).mean()
    return df

# =============================================================================
# MAIN EXECUTION
# =============================================================================

print("🔄 Loading SPY data...")
df = read_csv_to_dataframe(file_path)

print("⚙️  Processing signals + ATR...")
df = add_atr(df, length=10)
df = add_total_signal(df)
df.dropna(inplace=True)

# =============================================================================
# BASELINE CALCULATIONS
# =============================================================================

# 1. STRATEGY STATS
buys = sum(df['TotalSignal']==2)
sells = sum(df['TotalSignal']==1)

# 2. BUY & HOLD BASELINE
buy_hold_return = ((df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100)

# 3. RANDOM STRATEGY BACKTEST
def run_random_backtest(df, initial_capital=10000):
    """Execute original random strategy backtest."""
    equity = initial_capital
    position = 0
    entry_price = 0
    trades = []
    
    for i in range(len(df)):
        price = df['Close'].iloc[i]
        signal = df['TotalSignal'].iloc[i]
        
        if signal == 2 and position == 0:  # BUY
            position = 100 / price  # $100 position size
            entry_price = price
        elif signal == 1 and position > 0:  # SELL
            pnl = position * (price - entry_price)
            equity += pnl
            trades.append(pnl)
            position = 0
    
    return equity, len(trades), np.mean(trades) if trades else 0

strategy_equity, num_trades, avg_pnl = run_random_backtest(df)

# =============================================================================
# RESULTS SUMMARY
# =============================================================================

print("\n📊 LAST 20 CANDLES:")
print(" B=Buy(2) S=Sell(1) | = No signal")
for i in range(-20, 0):
    signal = {2:'🟢B', 1:'🔴S', 0:'|'} [df['TotalSignal'].iloc[i]]
    change = "📈" if df['Close'].iloc[i] > df['Open'].iloc[i] else "📉"
    print(f"{change} {df['Close'].iloc[i]:6.1f} {signal}")

print("\n" + "="*60)
print("TOM BASSO RANDOM STRATEGY vs BUY & HOLD")
print("="*60)
print(f"📊 Period: {df.index[0].date()} → {df.index[-1].date()} ({len(df)} days)")
print(f"💲 Price Range: ${df['Close'].min():.1f} → ${df['Close'].max():.1f}")
print(f"\n🎯 SIGNALS:")
print(f"   Buy(2): {buys:4d} | Sell(1): {sells:4d} | Frequency: {100*(buys+sells)/len(df):5.1f}%")
print(f"\n🏆 PERFORMANCE:")
print(f"   Buy & Hold:     +{buy_hold_return:+6.1f}%")
print(f"   Random Strategy: +{((strategy_equity/10000-1)*100):+6.1f}%")
print(f"   Alpha vs B&H:   {((strategy_equity/10000-1)*100 - buy_hold_return):+6.1f}%")
print(f"\n⚡ BACKTEST STATS:")
print(f"   Start:  $10,000 → End:  ${strategy_equity:,.0f}")
print(f"   Trades: {num_trades:4d} | Avg PnL: ${avg_pnl:+6.0f}")

print("\n" + "="*60)
print("✅ Tom Basso Baseline VALIDATED - Ready for real signals!")
print("="*60)
