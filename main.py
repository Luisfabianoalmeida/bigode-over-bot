import requests
import random
import time

BOT_TOKEN = "8544364550:AAGB37CwzJWVJt7DSafOH6DU28F9Wh2IgPA"
CHAT_ID = "6655882510"

def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    requests.post(url, data=payload)
    print("🚀 Alerta enviado!")

import requests
import random

def obter_dados_jogo():
    url = "https://api.sofascore.com/api/v1/sport/football/events/live"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        print("Erro ao buscar dados:", resposta.status_code)
        return None

    dados = resposta.json()
    jogos = dados.get("events", [])

    if not jogos:
        print("Nenhum jogo ao vivo agora.")
        return None

    # Filtra jogos com mais de 10 minutos
    jogos_validos = []
    for jogo in jogos:
        try:
            minuto = jogo["time"]["currentPeriodStartTimestamp"]
            if minuto > 600:  # +10 minutos
                jogos_validos.append(jogo)
        except:
            continue

    if not jogos_validos:
        return None

    # Escolhe um jogo aleatório dos que estão com ação
    jogo = random.choice(jogos_validos)
    mandante = jogo["homeTeam"]["name"]
    visitante = jogo["awayTeam"]["name"]
    liga = jogo["tournament"]["name"]
    placar_mandante = jogo["homeScore"]["current"]
    placar_visitante = jogo["awayScore"]["current"]
    minuto = (jogo.get("status", {}).get("description", "AO VIVO"))

    # busca estatísticas
    stats_url = f"https://api.sofascore.com/api/v1/event/{jogo['id']}/statistics"
    stats = requests.get(stats_url).json()

    home_shots = 0
    away_shots = 0
    if "statistics" in stats:
        for grupo in stats["statistics"]:
            for item in grupo["groups"]:
                if item["name"] == "Shots on target":
                    home_shots = item["statisticsItems"][0]["home"]
                    away_shots = item["statisticsItems"][0]["away"]

    return {
        "liga": liga,
        "mandante": mandante,
        "visitante": visitante,
        "placar_mandante": placar_mandante,
        "placar_visitante": placar_visitante,
        "minuto": minuto,
        "chutes_total": home_shots + away_shots
    }
def gerar_mensagem(dados):
    return f"""
⚽ <b>{dados['liga']}</b>
🏟️ {dados['mandante']} x {dados['visitante']}
⏱️ {dados['minuto']}
📊 Placar: {dados['placar_mandante']} x {dados['placar_visitante']}
🥅 Finalizações: {dados['chutes_total']}
🚨 <b>Pressão alta — possível Over Gols!</b>
"""

def main():
    while True:
        dados = obter_dados_jogo()
        if dados and dados["chutes_total"] >= 8:  # alerta só se tiver pressão
            mensagem = gerar_mensagem(dados)
            enviar_alerta(mensagem)
        time.sleep(60)

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
