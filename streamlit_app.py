import streamlit as st
import pandas as pd
import numpy as np

try:
    import yfinance as yf
except ImportError:
    st.error("yfinance not installed. Check requirements.txt")
    st.stop()

st.set_page_config(
    page_title=" Financial Crisis Detection",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def fetch_market_data(symbol: str, period: str = "30d") -> dict:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return {"error": f"No data found for symbol: {symbol}"}
        
        returns = hist['Close'].pct_change()
        volatility = returns.std() * np.sqrt(252) * 100
        
        current_price = hist['Close'].iloc[-1]
        price_change_30d = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
        
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "price_change_percent": round(price_change_30d, 2),
            "volatility_percent": round(volatility, 2),
            "volume": int(hist['Volume'].iloc[-1]),
            "data": hist,
            "returns": returns
        }
    except Exception as e:
        return {"error": str(e)}

def detect_crisis_signals(market_data: dict) -> dict:
    if "error" in market_data:
        return {"error": market_data["error"]}
    
    signals = []
    
    if market_data['volatility_percent'] > 20:
        signals.append(" High Volatility (>20%)")
    
    if market_data['price_change_percent'] < -5:
        signals.append(" Sharp Decline (>5%)")
    
    if market_data['price_change_percent'] < -2:
        signals.append(" Negative Momentum (<-2%)")
    
    return {
        "signals": signals,
        "signal_count": len(signals)
    }

def calculate_risk_score(signal_count: int) -> dict:
    risk_score = min(signal_count * 25, 100)
    
    if risk_score < 30:
        classification = " LOW"
        recommendation = "Continue monitoring"
    elif risk_score < 50:
        classification = " MODERATE"
        recommendation = "Pay attention"
    elif risk_score < 70:
        classification = " HIGH"
        recommendation = "Consider action"
    else:
        classification = " CRITICAL"
        recommendation = "Review urgently"
    
    return {
        "risk_score": risk_score,
        "classification": classification,
        "recommendation": recommendation
    }

def analyze_portfolio(symbols: list) -> dict:
    portfolio_data = []
    total_risk = 0
    high_risk_assets = 0
    
    for symbol in symbols:
        try:
            market_data = fetch_market_data(symbol.strip())
            if "error" not in market_data:
                signals = detect_crisis_signals(market_data)
                risk = calculate_risk_score(signals.get("signal_count", 0))
                
                portfolio_data.append({
                    "symbol": symbol,
                    "price": market_data['current_price'],
                    "volatility": market_data['volatility_percent'],
                    "risk_score": risk['risk_score'],
                    "classification": risk['classification']
                })
                
                total_risk += risk['risk_score']
                if risk['risk_score'] > 50:
                    high_risk_assets += 1
        except:
            pass
    
    if len(portfolio_data) == 0:
        return {"error": "No valid symbols in portfolio"}
    
    avg_portfolio_risk = total_risk / len(portfolio_data)
    
    if avg_portfolio_risk < 30:
        portfolio_rec = "Monitor"
    elif avg_portfolio_risk < 50:
        portfolio_rec = "Review"
    else:
        portfolio_rec = "Rebalance"
    
    return {
        "portfolio_data": portfolio_data,
        "portfolio_risk": round(avg_portfolio_risk, 2),
        "high_risk_assets": high_risk_assets,
        "recommendation": portfolio_rec
    }

st.markdown("""
    <style>
    .main { max-width: 1200px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title(" Financial Crisis Detection Agent")
st.markdown("*Real-Time Market Analysis & Risk Assessment*")
st.divider()

with st.sidebar:
    st.header(" Analysis Mode")
    mode = st.radio(
        "Select Analysis Mode:",
        ["Single Stock", "Portfolio Analysis", "Dashboard"]
    )

if mode == "Single Stock":
    st.header("Single Stock Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        symbol = st.text_input("Enter Stock Symbol", value="AAPL", placeholder="e.g., AAPL, TCS.NS")
    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button(" Analyze", use_container_width=True, type="primary")
    
    if analyze_btn and symbol:
        with st.spinner(f"Fetching data for {symbol}..."):
            market_data = fetch_market_data(symbol)
            
            if "error" in market_data:
                st.error(f"Error: {market_data['error']}")
            else:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Current Price", f"${market_data['current_price']}")
                with col2:
                    st.metric("30-Day Change", f"{market_data['price_change_percent']:.2f}%")
                with col3:
                    st.metric("Volatility", f"{market_data['volatility_percent']:.2f}%")
                with col4:
                    st.metric("Volume", f"{market_data['volume']:,}")
                
                st.divider()
                
                signals = detect_crisis_signals(market_data)
                risk = calculate_risk_score(signals["signal_count"])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Crisis Signals")
                    if signals["signals"]:
                        for signal in signals["signals"]:
                            st.write(signal)
                    else:
                        st.success(" No crisis signals detected")
                
                with col2:
                    st.subheader(" Risk Assessment")
                    st.metric("Risk Score", f"{risk['risk_score']}/100")
                    st.metric("Classification", risk['classification'])
                    st.write(f"**Recommendation:** {risk['recommendation']}")

elif mode == "Portfolio Analysis":
    st.header(" Portfolio Analysis")
    
    symbols_input = st.text_input(
        "Enter Stock Symbols (comma-separated)",
        value="AAPL,SPY,MSFT",
        placeholder="e.g., AAPL,TCS.NS,BTC-USD"
    )
    
    col1, col2 = st.columns([3, 1])
    with col2:
        analyze_btn = st.button(" Analyze Portfolio", use_container_width=True, type="primary")
    
    if analyze_btn and symbols_input:
        symbols = [s.strip() for s in symbols_input.split(",")]
        
        with st.spinner(f"Analyzing {len(symbols)} symbols..."):
            portfolio = analyze_portfolio(symbols)
            
            if "error" in portfolio:
                st.error(f"Error: {portfolio['error']}")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Portfolio Risk", f"{portfolio['portfolio_risk']}/100")
                with col2:
                    st.metric("High-Risk Assets", portfolio['high_risk_assets']")
                with col3:
                    st.metric("Recommendation", portfolio['recommendation'])
                
                st.divider()
                
                st.subheader(" Asset Breakdown")
                df = pd.DataFrame(portfolio['portfolio_data'])
                st.dataframe(df, use_container_width=True)

else:
    st.header(" Dashboard")
    st.info("Select specific symbols in Single Stock or Portfolio mode to see detailed analysis.")
    
    st.subheader(" Featured Symbols")
    featured = ["AAPL", "SPY", "BTC-USD"]
    
    cols = st.columns(3)
    for idx, symbol in enumerate(featured):
        with cols[idx]:
            try:
                market_data = fetch_market_data(symbol)
                if "error" not in market_data:
                    signals = detect_crisis_signals(market_data)
                    risk = calculate_risk_score(signals["signal_count"])
                    
                    st.metric(
                        symbol,
                        f"${market_data['current_price']}",
                        f"{market_data['price_change_percent']:.1f}%"
                    )
                    st.write(f"Risk: {risk['classification']}")
            except:
                st.write(f" {symbol} - Unable to fetch")

st.divider()
st.markdown("""
    ---
    **Built for:** Google-Kaggle AI Agents Competition  
    **Tech Stack:** Streamlit | yfinance | Pandas | Python  
    **Data Source:** Yahoo Finance
""")

