import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

# ==========================================
# 1. LIVE MARKET DATA INGESTION ENGINE
# ==========================================
def fetch_market_volatility(ticker, period="1y"):
    """
    Pulls real-world asset data to isolate market-implied risk regimes.
    Weather volatility directly drives energy price variance.
    """
    print(f"[+] Fetching live market data for {ticker}...")
    asset = yf.Ticker(ticker)
    df = asset.history(period=period)
    
    if df.empty:
        raise ValueError(f"No data returned for ticker {ticker}. Check internet connection.")
        
    # Calculate daily log returns
    df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # Annualize the historical volatility (252 trading days)
    ann_volatility = df['Returns'].std() * np.sqrt(252)
    latest_price = df['Close'].iloc[-1]
    
    return latest_price, ann_volatility

# ==========================================
# 2. THE TEMPERATURE SIMULATION ENGINE (OU PROCESS)
# ==========================================
def simulate_temperatures(base_temp, mean_reversion_speed, volatility, days, paths):
    """
    Simulates daily temperatures using a mean-reverting Ornstein-Uhlenbeck process.
    Weather cannot drift indefinitely like stocks; it always reverts to seasonal means.
    """
    dt = 1 / 365.0
    T = np.zeros((days, paths))
    T[0, :] = base_temp  # Initialize all simulated paths at current temperature
    
    for t in range(1, days):
        # SDE: dT = a*(Mean - T)*dt + sigma*dW
        noise = np.random.normal(0, 1, paths)
        dT = mean_reversion_speed * (base_temp - T[t-1, :]) * dt + volatility * np.sqrt(dt) * noise
        T[t, :] = T[t-1, :] + dT
        
    return T

# ==========================================
# 3. QUANTITATIVE DERIVATIVE PRICING ENGINE
# ==========================================
def price_weather_derivative(temp_matrix, strike_hdd, tick_value, risk_free_rate, days):
    """
    Translates daily temperatures into Heating Degree Days (HDD) payouts.
    Uses Monte Carlo integration to find the risk-adjusted present value.
    """
    # Calculate HDD for each day across all paths: Max(0, 65 - Temperature)
    hdd_matrix = np.maximum(0, 65 - temp_matrix)
    
    # Cumulative HDDs for the contract period per path
    cumulative_hdd = np.sum(hdd_matrix, axis=0)
    
    # Option Payoff: Max(0, Cumulative HDD - Strike) * Dollar Value per HDD unit
    payoffs = np.maximum(0, cumulative_hdd - strike_hdd) * tick_value
    
    # Discount back to present value using continuous compounding
    discount_factor = np.exp(-risk_free_rate * (days / 365.0))
    present_value_price = np.mean(payoffs) * discount_factor
    
    return present_value_price

# ==========================================
# 4. EXECUTION ORCHESTRATOR
# ==========================================
if __name__ == "__main__":
    print("="*60)
    print(" QUANTITATIVE WEATHER DERIVATIVE PRICER (WTI vs NAT GAS) ")
    print("="*60)
    
    # Step 4a: Load Live Market Regimes
    try:
        wti_price, wti_vol = fetch_market_volatility("CL=F")
        natgas_price, natgas_vol = fetch_market_volatility("NG=F")
    except Exception as e:
        print(f"[-] Data error: {e}. Falling back to baseline metrics.")
        wti_price, wti_vol = 75.0, 0.35
        natgas_price, natgas_vol = 2.50, 0.65

    print(f"\n[!] Live Market Status:")
    print(f"    WTI Crude Oil:  Price = ${wti_price:.2f} | Implied Weather Volatility = {wti_vol*100:.2f}%")
    print(f"    Natural Gas:    Price = ${natgas_price:.2f}  | Implied Weather Volatility = {natgas_vol*100:.2f}%")

    # Step 4b: Set Contract Specifications
    STRIKE_HDD = 150      # Target heating degree days threshold
    TICK_VALUE = 20       # $20 payout per HDD over the strike
    RISK_FREE_RATE = 0.045 # 4.5% risk-free rate (US Treasuries)
    SIM_DAYS = 30         # 1-month contract duration
    NUM_PATHS = 10000     # Monte Carlo trial paths
    
    # Base baseline weather profile (e.g., winter transition day at 45°F)
    CURRENT_TEMP = 45.0
    SPEED_OF_MEAN_REVERSION = 2.5 

    print(f"\n[+] Executing Monte Carlo Pricing Simulations ({NUM_PATHS} paths)...")
    
    # Step 4c: Run WTI Environment Simulation
    wti_temps = simulate_temperatures(CURRENT_TEMP, SPEED_OF_MEAN_REVERSION, wti_vol*10, SIM_DAYS, NUM_PATHS)
    wti_derivative_price = price_weather_derivative(wti_temps, STRIKE_HDD, TICK_VALUE, RISK_FREE_RATE, SIM_DAYS)
    
    # Step 4d: Run Natural Gas Environment Simulation (Typically higher weather sensitivity)
    natgas_temps = simulate_temperatures(CURRENT_TEMP, SPEED_OF_MEAN_REVERSION, natgas_vol*10, SIM_DAYS, NUM_PATHS)
    natgas_derivative_price = price_weather_derivative(natgas_temps, STRIKE_HDD, TICK_VALUE, RISK_FREE_RATE, SIM_DAYS)

    print("="*60)
    print(" FINAL DERIVATIVE VALUATION COMPARISON ")
    print("="*60)
    print(f" Weather Contract Price under WTI Regime:        ${wti_derivative_price:.2f}")
    print(f" Weather Contract Price under Nat Gas Regime:    ${natgas_derivative_price:.2f}")
    print("="*60)
    print("[Success] Models evaluated successfully.")
