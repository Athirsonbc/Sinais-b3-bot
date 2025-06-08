import os
import time
import yfinance as yf
import requests

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def buscar_yahoo(ticker):
    try:
        dados = yf.Ticker(ticker + '.SA')
        hist = dados.history(period="1d", interval="5m")
        if len(hist) < 3:
            return None
        ultimos = hist.tail(3)['Close'].tolist()
        return ultimos
    except:
        return None

def buscar_alpha(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}.SA&interval=5min&apikey={ALPHA_KEY}"
        resp = requests.get(url).json()
        ts = resp.get("Time Series (5min)", {})
        valores = list(ts.values())[:3]
        if len(valores) < 3:
            return None
        closes = [float(x["4. close"]) for x in valores]
        return closes[::-1]
    except:
        return None

def buscar_dados_reais(ticker):
    dados = buscar_yahoo(ticker)
    if dados:
        return dados
    time.sleep(12)  # evitar limite da Alpha Vantage
    return buscar_alpha(ticker)
