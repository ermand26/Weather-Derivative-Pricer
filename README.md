# Quantitative Weather Derivative Pricer

A Python-based quantitative engine that prices weather derivatives (Heating Degree Day options) by matching simulations against real-time volatility regimes in **WTI Crude Oil** and **Natural Gas**.

## How It Works
1. **Live Data Collection**: Uses `yfinance` to pull asset prices and evaluate current annualized volatility levels.
2. **Stochastic Weather Modeling**: Simulates temperature pathways using a mean-reverting **Ornstein-Uhlenbeck Process**.
3. **Derivative Valuation**: Integrates daily payoffs to evaluate an HDD Call Option via a multi-path **Monte Carlo Simulation Engine**.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python pricer.py
```
