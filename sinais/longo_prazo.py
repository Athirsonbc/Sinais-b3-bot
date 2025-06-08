import json
import random
import time
from services.market_data import buscar_dados_reais
from utils.gale import calcular_gales

def verificar_longo_prazo():
    sinais = []
    try:
        with open('data/ativos_longo.json', 'r') as f:
            ativos = json.load(f)
    except:
        return []

    for ticker in ativos:
        closes = buscar_dados_reais(ticker)
        if not closes:
            continue

        variacao = round((closes[-1] - closes[0]) / closes[0] * 100, 2)
        chance = 70 + abs(variacao)
        chance = min(chance, 95)

        if chance >= 75 and random.random() < 0.05:
            gale = calcular_gales(chance)
            sinais.append({
                "ativo": ticker,
                "tipo": "COMPRA",
                "chance": round(chance, 2),
                "duracao": "longo prazo",
                "estrategia": {
                    "entrada": f"{gale['entrada']}%",
                    "minimo": f"{round(gale['entrada'], 2)}% da banca"
                }
            })

        time.sleep(12)  # Respeito aos limites da API
    return sinais
