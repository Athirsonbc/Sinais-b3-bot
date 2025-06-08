import json, requests, time
from os import getenv
from dotenv import load_dotenv
load_dotenv()

API_KEY = getenv("ALPHA_VANTAGE_KEY")

def validar_ativos(input_file, output_file):
    with open(input_file) as f:
        ativos = json.load(f).get("ativos", [])

    validos = []
    for a in ativos:
        ticker = a + ".SA"
        print(f"Validando {ticker} ...", end="")
        resp = requests.get("https://www.alphavantage.co/query", params={
            "function":"TIME_SERIES_DAILY", "symbol":ticker, "apikey":API_KEY})
        data = resp.json()
        ok = "Time Series (Daily)" in data
        print(" OK" if ok else " ✗")
        if ok: validos.append(a)
        time.sleep(12)

    with open(output_file, "w") as f:
        json.dump({"ativos": validos}, f, indent=2)

    print(f"\n✔️ Salvos {len(validos)} ativos válidos em {output_file}")

if __name__ == "__main__":
    validar_ativos("data/ativos.json","data/ativos_validados.json")
    validar_ativos("data/ativos_longo.json","data/ativos_longo_validos.json")
