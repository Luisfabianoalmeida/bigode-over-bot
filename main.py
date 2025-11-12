
import requestes
import random
import time

BOT_TOKEN = "COLE_SEU_TOKEN_AQUI"
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
        "posse_ma…
[20:52, 11/11/2025] Luis Fabiano: import requests
import random
import time

BOT_TOKEN = "COLE_SEU_TOKEN_AQUI"
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
        "posse_mandante": random.randint(45, 70),
        "posse_visitante": random.randint(30, 55),
        "chutes_mandante": random.randint(0, 8),
        "chutes_visitante": random.randint(0, 4),
        "chutes_no_gol_mandante": random.randint(0, 3),
        "chutes_no_gol_visitante": random.randint(0, 2),
        "escanteios_mandante": random.randint(0, 5),
        "escanteios_visitante": random.randint(0, 3)
    }

def analisar_jogo(dados):
    diferenca_chutes = dados["chutes_mandante"] - dados["chutes_visitante"]
    posse_domínio = dados["posse_mandante"] > 55
    escanteios_altos = dados["escanteios_mandante"] >= 3
    jogo_empatado = (dados["placar_mandante"] == 0 and dados["placar_visitante"] == 0)
    minuto_certo = 10 <= dados["minuto"] <= 35

    if posse_domínio and diferenca_chutes >= 3 and escanteios_altos and jogo_empatado and minuto_certo:
        mensagem = f"""
💎 <b>[Robô Over Gols - Bigode Premium detectou uma chance quente!]</b>

🏟 {dados['liga']}
⚽ {dados['mandante']} vs {dados['visitante']}
🕐 {dados['minuto']} minutos do 1º tempo
🔢 Placar: {dados['placar_mandante']} - {dados['placar_visitante']}

📊 Dados do jogo:
* Posse de bola: {dados['posse_mandante']}% - {dados['posse_visitante']}%
* Chutes: {dados['chutes_mandante']} - {dados['chutes_visitante']}
* Chutes no gol: {dados['chutes_no_gol_mandante']} - {dados['chutes_no_gol_visitante']}
* Escanteios: {dados['escanteios_mandante']} - {dados['escanteios_visitante']}

🔥 <b>Sinal: Mais 0.5 gol no primeiro tempo</b>

🎲 Superbet
💬 Jogue com responsabilidade 🔞
"""
        enviar_alerta(mensagem)

if _name_ == "_main_":
    print("🤖 Robô Over Gols - Bigode Premium iniciado...")
    while True:
        jogo = obter_dados_jogo()
        analisar_jogo(jogo)
        time.sleep(15)
