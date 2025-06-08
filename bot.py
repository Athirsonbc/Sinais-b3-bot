import os
import time
import telebot
import json
from dotenv import load_dotenv
from sinais.analise import analisar_sinais
from sinais.longo_prazo import verificar_longo_prazo
from utils.formatador import formatar_mensagem, mensagem_monitoramento

# Carrega variáveis de ambiente
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("❌ ERRO: TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não configurados no .env")
    exit(1)

bot = telebot.TeleBot(TOKEN)

ultima_entrada = time.time()

def carregar_ativos(caminho):
    try:
        with open(caminho, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar {caminho}: {e}")
        return []

def executar_bot():
    global ultima_entrada

    print("🤖 Bot Fatrades iniciado com sucesso!")

    ativos_validos = carregar_ativos("data/ativos_validos.json")
    ativos_longo_validos = carregar_ativos("data/ativos_longo_validos.json")

    if not ativos_validos:
        print("⚠️ Nenhum ativo válido encontrado para sinais normais.")
    if not ativos_longo_validos:
        print("⚠️ Nenhum ativo válido encontrado para sinais de longo prazo.")

    while True:
        try:
            print("🔍 Analisando sinais normais...")
            sinais = analisar_sinais(ativos_validos)

            if sinais:
                for sinal in sinais:
                    msg = formatar_mensagem(sinal)
                    bot.send_message(CHAT_ID, msg)
                    ultima_entrada = time.time()
            else:
                tempo_sem_entrada = time.time() - ultima_entrada
                if tempo_sem_entrada >= 1200:
                    bot.send_message(CHAT_ID, mensagem_monitoramento())
                    ultima_entrada = time.time()

            print("📈 Analisando sinais de longo prazo...")
            sinais_longo = verificar_longo_prazo(ativos_longo_validos)
            for sinal in sinais_longo:
                bot.send_message(CHAT_ID, formatar_mensagem(sinal))

        except Exception as e:
            print(f"🚨 Erro durante execução: {e}")

        print("⏳ Aguardando 5 minutos para nova análise...")
        time.sleep(300)

if __name__ == "__main__":
    executar_bot()
