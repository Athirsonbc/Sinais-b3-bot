import os
import time
import telebot
from dotenv import load_dotenv
from sinais.analise import analisar_sinais
from sinais.longo_prazo import verificar_longo_prazo
from utils.formatador import formatar_mensagem, mensagem_monitoramento

# Carrega variáveis de ambiente
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # ID do grupo ou canal

bot = telebot.TeleBot(TOKEN)

ultima_entrada = time.time()  # timestamp da última entrada enviada

def executar_bot():
    global ultima_entrada
    print("🔁 Bot Fatrades rodando continuamente...")

    while True:
        print("🔍 Analisando sinais normais...")
        sinais = analisar_sinais()

        if sinais:
            for sinal in sinais:
                msg = formatar_mensagem(sinal)
                bot.send_message(CHAT_ID, msg)
                ultima_entrada = time.time()
        else:
            tempo_sem_entrada = time.time() - ultima_entrada
            if tempo_sem_entrada >= 1200:  # 20 minutos
                bot.send_message(CHAT_ID, mensagem_monitoramento())
                ultima_entrada = time.time()

        print("🧠 Analisando sinais de longo prazo...")
        sinais_longo_prazo = verificar_longo_prazo()
        for sinal in sinais_longo_prazo:
            bot.send_message(CHAT_ID, formatar_mensagem(sinal))

        time.sleep(300)  # Espera 5 minutos antes da próxima análise

if __name__ == "__main__":
    executar_bot()
