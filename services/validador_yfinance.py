import yfinance as yf
import json

CAMINHO = 'data/ativos_longo.json'  # troque para 'data/ativos.json' se for validar os normais

with open(CAMINHO, 'r') as f:
    ativos = json.load(f)

ativos_validos = []

print("Validando ativos...\n")
for ativo in ativos:
    try:
        ticker = yf.Ticker(ativo)
        hist = ticker.history(period="1d")
        if not hist.empty:
            print(f"[✔] {ativo} válido.")
            ativos_validos.append(ativo)
        else:
            print(f"[X] {ativo} inválido ou sem dados.")
    except Exception as e:
        print(f"[!] Erro ao validar {ativo}: {e}")

with open(CAMINHO, 'w') as f:
    json.dump(ativos_validos, f, indent=2, ensure_ascii=False)

print(f"\n✅ {len(ativos_validos)} ativos válidos salvos em {CAMINHO}")
