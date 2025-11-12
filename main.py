import requests
import random
import time

BOT_TOKEN = "8544364550:AAGB37CwzJWVJt7DSaf0H6DU28F9wh2IgPA"
CHAT_ID = "6655882510"

def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    requests.post(url, data=payload)
    print("🚀 Alerta enviado!")

def obter_dados_jogo():
    return {
        "liga": random.choice(["UEFA Champions League", "Copa do Brasil", "Premier League"]),
        "mandante": random.choice(["AS Roma", "Flamengo", "Palmeiras", "Chelsea"]),
        "visitante": random.choice(["Valerenga", "Corinthians", "Atlético-MG", "Liverpool"]),
        "minuto": random.randint(5, 40),
        "placar_mandante": 0,
        "placar_visitante": 0,
        "posse_mandante": random.randint(30, 70)
    }

def gerar_mensagem(dados):
    return f"""
⚽ <b>{dados['liga']}</b>
🏟️ {dados['mandante']} x {dados['visitante']}
⏱️ Minuto: {dados['minuto']}
📊 Posse: {dados['posse_mandante']}%
📢 Alerta gerado automaticamente!
"""

def main():
    while True:
        dados = obter_dados_jogo()
        mensagem = gerar_mensagem(dados)
        enviar_alerta(mensagem)
        time.sleep(60)
        
# --- Teste manual de envio ---
enviar_alerta("🚀 Teste: o Robô Over Gols está online e ativo!")
        

# --- Mantém o app ativo no Render ---
from flask import Flask
import threading, os

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Robô Over Gols ativo e enviando alertas no Telegram!"

if __name__ == "__main__":
    t = threading.Thread(target=main)
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
