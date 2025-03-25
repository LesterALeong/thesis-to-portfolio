# [Thesis to Portfolio](https://thesistoportfolio.streamlit.app/)

**LLM-Powered Investment Assistant** built using Streamlit, OpenAI GPT-4o mini, Financial Modeling Prep (FMP), and yFinance.

This tool is designed to emulate an institutional investment research assistant by:

- Summarizing SEC filings and earnings calls into structured investment theses
- Aggregating sentiment from news and public sources
- Analyzing portfolio-level risk and return from user-uploaded data
- Generating thematic ETF-style baskets based on natural language input

## Features

### 1. Investment Thesis Generator
- Input a stock ticker
- Fetches the latest 10-K or earnings call transcript
- GPT-4o mini generates bull and bear cases as an investment thesis

### 2. Sentiment Signal Analyzer
- Analyzes recent news headlines for a stock
- Summarizes sentiment and market themes using GPT

### 3. Portfolio Analyzer
- Upload a CSV with stock holdings (Ticker, Shares, Cost Basis)
- Calculates 6-month return and volatility per position using yFinance
- Downloadable CSV report

### 4. Thematic ETF Generator
- Input any investment theme (e.g., "AI Infrastructure", "China Tech Recovery")
- GPT generates a 10-stock basket and rationalizes selections

## Technologies Used
- [Streamlit](https://streamlit.io/)
- [OpenAI API (GPT-4o mini)](https://platform.openai.com/docs)
- [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/)
- [yFinance](https://github.com/ranaroussi/yfinance)

## Setup

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/thesis-to-portfolio.git
cd thesis-to-portfolio
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. When prompted in the sidebar, enter your:
- OpenAI API Key
- Financial Modeling Prep API Key

## File Structure
```
thesis-to-portfolio/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # You're reading this
```

## Example Inputs
**Portfolio CSV Format:**
```
Ticker,Shares,Cost Basis
AAPL,10,145.00
MSFT,5,300.00
TSLA,7,210.00
```

## License
MIT License

## Author
Lester A. Leong  
[LinkedIn](https://www.linkedin.com/in/lester-a-leong/)
[Medium](https://www.medium.com/@LesterLeong)

For professional inquiries, feel free to reach out via LinkedIn, Medium, or submit issues via GitHub.
