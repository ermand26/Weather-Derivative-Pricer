# Quantitative Weather Derivative Pricing Results

This document presents the structural metrics and valuation comparisons derived from the Monte Carlo pricing engine simulation.

## 📊 Live Market & Valuation Metrics

| Metric | Value |
| :--- | :--- |
| **WTI Crude Oil Price (CL=F)** | $80.95 |
| **WTI Implied Weather Volatility** | 52.26% |
| **Natural Gas Price (NG=F)** | $2.90 |
| **Natural Gas Implied Weather Volatility** | 101.67% |
| **Monte Carlo Pricing Simulations** | 10,000 Paths |
| **Weather Contract Price (WTI Regime)** | $8,964.36 |
| **Weather Contract Price (Nat Gas Regime)** | $8,950.32 |

---

## 🔍 Structural Analysis & Interpretation

### 1. The Volatility Paradox
The model reveals a critical structural phenomenon: **Natural Gas exhibits nearly double the Implied Weather Volatility (101.67%) compared to WTI Crude Oil (52.26%)**, yet their final risk-neutral contract valuations remain almost identical (a delta of only $14.04).

* **Asset Price Independence:** Weather derivative payoffs (CME-style HDD/CDD contracts) are strictly driven by temperature indices rather than underlying asset prices ($80.95 vs $2.90). 
* **Tail-Risk Distribution:** The extreme volatility in the Natural Gas regime stretches the fat-tails of the simulated weather distributions. However, when averaged across 10,000 risk-neutral Monte Carlo paths, the expected payoff tightly converges back to the structural weather matrix baseline.

### 🏢 Hedging Suitability
* **Natural Gas Regime ($8,950.32):** Optimal for **utility grids and power plants** seeking to hedge volume/demand risk (e.g., a warm winter destroying heating fuel sales).
* **WTI Crude Oil Regime ($8,964.36):** Optimal for **refineries and upstream producers** looking to hedge operational/logistical disruptions (e.g., localized freeze-offs shutting down physical production infrastructure).
