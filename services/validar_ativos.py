import json
import yfinance as yf
import requests
import time
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_KEY = getenv("ALPHA_VANTAGE_API_KEY")

def validar_ativo_yf(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except Exception:
        return False

def validar_ativo_av(ticker):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()
        return "Time Series (Daily)" in data
    except Exception:
        return False

def validar_ativos():
    with open("data/ativos.json") as f:
        ativos = json.load(f)

    ativos_validos = []
    for ativo in ativos:
        print(f"Validando {ativo}...")
        if validar_ativo_yf(ativo):
            ativos_validos.append(ativo)
            print(f"[OK] {ativo} válido pelo Yahoo Finance.")
        else:
            print(f"[!] {ativo} falhou no Yahoo. Testando Alpha Vantage...")
            if validar_ativo_av(ativo):
                ativos_validos.append(ativo)
                print(f"[OK] {ativo} válido pela Alpha Vantage.")
            else:
                print(f"[X] {ativo} inválido nas duas fontes.")
        time.sleep(12)  # evitar limites de API da Alpha Vantage

    with open("data/ativos_validos.json", "w") as f:
        json.dump(ativos_validos, f, indent=2)

    print(f"\nValidação concluída. {len(ativos_validos)} ativos válidos salvos em 'data/ativos_validos.json'.")

if __name__ == "__main__":
    validar_ativos()
