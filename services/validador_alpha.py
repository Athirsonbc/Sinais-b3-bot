import json
import requests
import time
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_KEY = getenv("ALPHA_VANTAGE_API_KEY")

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
        if validar_ativo_av(ativo):
            ativos_validos.append(ativo)
            print(f"[OK] {ativo} válido.")
        else:
            print(f"[X] {ativo} inválido ou delistado.")
        time.sleep(12)  # Respeita o limite de 5 chamadas por minuto da Alpha

    with open("data/ativos_validos.json", "w") as f:
        json.dump(ativos_validos, f, indent=2)

    print(f"\n{len(ativos_validos)} ativos válidos salvos em data/ativos_validos.json")

if __name__ == "__main__":
    validar_ativos()
