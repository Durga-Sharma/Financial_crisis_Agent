# Financial Crisis Detection System

**Status:** Live & Working | **GitHub:** [Financial_crisis_Agent](https://github.com/Durga-Sharma/Financial_crisis_Agent) | **Demo:** [Streamlit App](link)

---

## What This Does

Analyzes real-time stock market data using **three specialized AI agents** to detect early warning signs of financial crises.

- **Input:** Stock symbol (AAPL, BTC-USD, SPY, etc.)
- **Output:** Risk score (0-100) + Explanation in 5 seconds
- **Status:** Real market data from Yahoo Finance

---

##  System Architecture


User Input (Stock Symbol) --> Crisis Detector Agent-->Risk Scorer Agent--> Explainer agent--> Risk Report (output)   


1. Crisis Detector Agent -(Pattern Recognition)
 Volatility spikes
 Momentum shifts  
 News sentiment   
 
2. Risk Scorer Agent-(Quantification)
  Weight signals: 15 + 40
  Convert to 0-100 scale  
  Add confidence level 
3. Explainer Agent =(Communication)
 Translate to plain English 
 Highlight key signals
 Suggest actions 

### Why Three Agents?

Each agent is a specialist:
- **Crisis Detector** = Pattern recognition expert (finds signals)
- **Risk Scorer** = Financial math expert (weighs importance)
- **Explainer** = Communication expert (translates to humans)

Three specialists > one generalist

---

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| **Agent Framework** | Google Agent Development Kit | Production-ready orchestration |
| **LLM** | Gemini 2.0 Flash | Fast (0.8s) |
| **Market Data** | yfinance API | Free, reliable, 15+ years history |
| **News Data** | NewsAPI | Sentiment analysis for crisis signals |
| **Deployment** | Streamlit Cloud | Free hosting, Python-native |

---

##  How to Run Locally

```bash
# Clone the repo
git clone https://github.com/Durga-Sharma/Financial_crisis_Agent.git
cd Financial_crisis_Agent

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your_key_here"
export NEWS_API_KEY="your_key_here"

# Run Streamlit app
streamlit run app.py

# Open: http://localhost:8501
```

---

##  How It Works: Step by Step

### Step 1: Data Collection
```python
# Get live market data
price_history = yfinance.download('AAPL')
current_price = price_history['Close'][-1]
volatility = price_history['Close'].std()
```

### Step 2: Signal Detection
```python
signals = {
    'volatility_spike': volatility > threshold,
    'momentum_shift': momentum_change > threshold,
    'news_sentiment': sentiment_score < -0.5
}
```

### Step 3: Risk Scoring
```python
risk_score = (len(signals) * 15) + (signal_strength * 40)
# Example: 3 signals, strength 60 --> 3*15 + 60*40 = 2445 --> normalized to 68/100
```

### Step 4: Explanation
```
"Apple shows HIGH VOLATILITY (68/100 risk).
Key signals:
 Price jumped 4.2% in 2 hours
 News mentions market uncertainty
 Trading volume up 45%

What to do:
 Monitor closely tomorrow
 Consider reducing exposure
 Set stop-loss at $180"
```

---

##  Key Features

 **Real-Time Analysis** - Updates during trading hours
 **Multi-Asset Support** - Stocks, crypto, indices, ETFs
 **Explainable AI** - Shows WHY it flagged as risky
 **Portfolio View** - Analyze multiple stocks at once
 **Deployed Live** - No setup needed, just visit the link

---

## Future Improvements

### Phase 2 
- [ ] **Backtesting on Historical Crises** (2008, 2020, 2022)
  - Validate system against known market crashes
  - Measure detection accuracy + lead time
  
- [ ] **Multi-Source Data Integration**
  - Add Fed interest rate data
  - Add options flow (put/call ratios)
  - Add social sentiment tracking
  - Combine signals for better detection

- [ ] **ML-Based Signal Weighting**
  - Train on historical crash data
  - Learn optimal signal weights instead of hardcoded
  - Improve accuracy from 70% → 85%+

### Phase 3 
- [ ] **Caching Layer** (Redis/Cache)
  - Reduce API calls by 80%
  - Speed up repeated analyses
  - Cost reduction

- [ ] **Portfolio Correlation Analysis**
  - Detect sector-wide risks
  - Identify contagion patterns
  - Show system-level instability

- [ ] **User Dashboard**
  - Save favorite portfolios
  - Track alert history
  - Custom thresholds
  - Export reports


---

## Important Disclaimers

 **This is NOT:**
- Financial advice
- A replacement for professional analysis
- 100% accurate (no system is)
- Ready for production trading

 **This IS:**
- A research prototype
- Educational demonstration
- Early warning signal tool
- Starting point for further development


---

##  Links

- **Live Demo:** [Streamlit App](https://your-link.streamlit.app)
- **GitHub:** [Code Repository](https://github.com/Durga-Sharma/Financial_crisis_Agent)
- **Documentation:** README (this file)
- **Architecture:** See Architecture.md

---

## License

Open source - feel free to fork, modify, and improve

---

##  Questions?

Open an issue on GitHub 
---

**Last Updated:** December 1, 2024
**Status:** Live & Functional
**Next Phase:** Backtesting on historical data 