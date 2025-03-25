import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import openai
import datetime
from io import StringIO

# --- Set up UI layout ---
st.set_page_config(page_title="LLM Investment Assistant", layout="wide")
st.title("LLM Investment Assistant")

# --- API Keys ---
st.sidebar.header("API Keys")
fmp_api_key = st.sidebar.text_input("FMP API Key", type="password")
openai_api_key = st.sidebar.text_input("OpenAI API Key (GPT-4o Mini)", type="password")
openai.api_key = openai_api_key

# --- Utility Functions ---
def fetch_fmp_10k(ticker):
    url = f"https://financialmodelingprep.com/api/v3/sec_filings/{ticker}?type=10-K&limit=1&apikey={fmp_api_key}"
    response = requests.get(url)
    filings = response.json()
    if filings:
        return filings[0]['finalLink']
    return None

def fetch_fmp_earnings_call(ticker):
    url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?limit=1&apikey={fmp_api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['content']
    return None

def summarize_text(text, prompt):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text[:12000]}  # truncate for token limits
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o", messages=messages, temperature=0.3
    )
    return response.choices[0].message.content

def fetch_news_sentiment(ticker):
    url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=5&apikey={fmp_api_key}"
    response = requests.get(url)
    articles = response.json()
    if not articles:
        return "No recent news found."
    headlines = "\n".join([a['title'] for a in articles])
    return summarize_text(headlines, "Summarize the sentiment and main takeaways from these stock news headlines.")

def analyze_portfolio(df):
    results = []
    for _, row in df.iterrows():
        ticker = row['Ticker']
        try:
            data = yf.Ticker(ticker).history(period="6mo")
            ret = data['Close'].pct_change().mean() * 252
            vol = data['Close'].pct_change().std() * (252**0.5)
            results.append({"Ticker": ticker, "6M Return": round(ret * 100, 2), "Volatility": round(vol * 100, 2)})
        except Exception:
            results.append({"Ticker": ticker, "6M Return": "N/A", "Volatility": "N/A"})
    return pd.DataFrame(results)

def generate_etf_from_theme(theme):
    prompt = f"Given the investment theme: '{theme}', suggest 10 related U.S. stocks and explain why each was selected."
    return summarize_text("", prompt)

# --- App Tabs ---
tabs = st.tabs(["Investment Thesis", "Sentiment Signals", "Portfolio Analyzer", "Thematic ETF Generator"])

# --- Tab 1: Investment Thesis ---
with tabs[0]:
    st.subheader("Generate Thesis from 10-K or Earnings Call")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)")
    if st.button("Fetch & Summarize"):
        with st.spinner("Fetching data and summarizing with GPT..."):
            content = fetch_fmp_earnings_call(ticker)
            if not content:
                link = fetch_fmp_10k(ticker)
                content = requests.get(link).text if link else None
            if content:
                thesis = summarize_text(content, "Summarize this earnings/filing into an investment thesis with bull/bear case.")
                st.text_area("Investment Thesis", thesis, height=300)
            else:
                st.error("No content found for this ticker.")

# --- Tab 2: Sentiment Signals ---
with tabs[1]:
    st.subheader("Recent News & Market Sentiment")
    sentiment_ticker = st.text_input("Enter Ticker for Sentiment Analysis")
    if st.button("Analyze Sentiment"):
        with st.spinner("Analyzing news sentiment with GPT..."):
            sentiment = fetch_news_sentiment(sentiment_ticker)
            st.text_area("Sentiment Summary", sentiment, height=300)

# --- Tab 3: Portfolio Analyzer ---
with tabs[2]:
    st.subheader("Upload Portfolio CSV")
    uploaded_file = st.file_uploader("Upload CSV with columns: Ticker, Shares, Cost Basis")
    if uploaded_file:
        df_portfolio = pd.read_csv(uploaded_file)
        st.write("Uploaded Portfolio:", df_portfolio)
        results = analyze_portfolio(df_portfolio)
        st.write("Portfolio Analysis:", results)
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button("Download Portfolio Analysis CSV", csv, "portfolio_analysis.csv")

# --- Tab 4: Thematic ETF Generator ---
with tabs[3]:
    st.subheader("From Theme to ETF")
    theme_input = st.text_input("Enter Investment Theme (e.g., AI Infrastructure, Clean Energy, China Tech Recovery)")
    if st.button("Generate ETF"):
        with st.spinner("Generating ETF idea with GPT..."):
            etf_output = generate_etf_from_theme(theme_input)
            st.text_area("Thematic ETF Output", etf_output, height=400)
