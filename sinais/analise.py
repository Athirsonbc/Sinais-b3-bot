import json
import random
import requests
from utils.calcular_chance import calcular_chance
from utils.alpha_rotator import get_alpha_key

def analisar_sinais():
    try:
        with open("data/ativos_validos.json", "r") as f:
            ativos = json.load(f)
    except:
        return []

    sinais_encontrados = []
    for ativo in ativos:
        try:
            key = get_alpha_key()
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ativo}&interval=5min&apikey={key}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if "Time Series (5min)" not in data:
                print(f"[X] {ativo}: Erro ou limite da API")
                continue

            series = list(data["Time Series (5min)"].values())
            if len(series) < 2:
                continue

            open_price = float(series[1]["1. open"])
            close_price = float(series[0]["4. close"])
            chance = calcular_chance(open_price, close_price)

            if chance >= 70:
                sinais_encontrados.append({
                    "ativo": ativo,
                    "entrada": close_price,
                    "chance": chance,
                    "tipo": "COMPRA" if close_price > open_price else "VENDA"
                })

        except Exception as e:
            print(f"[!] Erro ao analisar {ativo}: {e}")
            continue

    return sinais_encontrados
