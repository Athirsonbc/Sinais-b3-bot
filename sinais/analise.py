import json
import time
from utils.gale import calcular_gales
from services.market_data import buscar_dados_reais

def analisar_sinais():
    sinais = []
    with open('data/ativos.json', 'r') as f:
        ativos = json.load(f)

    for ticker in ativos:
        closes = buscar_dados_reais(ticker)
        if not closes:
            continue

        tendencia = "alta" if closes[-1] > closes[0] else "baixa"
        variacao = round((closes[-1] - closes[0]) / closes[0] * 100, 2)
        chance = 65 + abs(variacao) * 2
        chance = min(chance, 95)

        if chance >= 70:
            tipo = "COMPRA" if tendencia == "alta" else "VENDA"
            gale = calcular_gales(chance)
            sinais.append({
                "ativo": ticker,
                "tipo": tipo,
                "chance": round(chance, 2),
                "duracao": 15,
                "estrategia": gale
            })

        time.sleep(12)  # Limitação da API
    return sinais
