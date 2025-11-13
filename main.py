import requests
import time
from flask import Flask

# ======================================================
# CONFIGURAÇÕES — COLOQUE SEUS DADOS AQUI
# ======================================================
BOT_TOKEN = "8544364550:AAGB37CwzJWVJt7DSafOH6DU28F9Wh2IgPA"
CHAT_ID = "6655882510"


# ======================================================
# FUNÇÃO PARA ENVIAR MENSAGEM NO TELEGRAM
# ======================================================
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except:
        pass


# ======================================================
# PEGAR TODOS OS JOGOS AO VIVO
# ======================================================
def get_live_games():
    url = "https://api.sofascore.com/api/v1/sport/football/events/live"
    r = requests.get(url, timeout=5)

    if r.status_code != 200:
        return []

    data = r.json()
    return data.get("events", [])


# ======================================================
# PEGAR ESTATÍSTICAS DE UM JOGO
# ======================================================
def get_stats(event_id):
    url = f"https://api.sofascore.com/api/v1/event/{event_id}/statistics"
    r = requests.get(url, timeout=5)

    if r.status_code != 200:
        return None

    data = r.json()

    stats = {
        "shots_total": 0,
        "shots_on_target": 0,
        "corners": 0,
        "dangerous_attacks": 0
    }

    if "statistics" in data:
        for group in data["statistics"]:
            for item in group["groups"]:
                name = item["name"]

                # Finalizações totais
                if name == "Total shots":
                    stats["shots_total"] = (
                        item["statisticsItems"][0]["home"] +
                        item["statisticsItems"][0]["away"]
                    )

                # Finalizações no alvo
                if name == "Shots on target":
                    stats["shots_on_target"] = (
                        item["statisticsItems"][0]["home"] +
                        item["statisticsItems"][0]["away"]
                    )

                # Escanteios
                if name == "Corner kicks":
                    stats["corners"] = (
                        item["statisticsItems"][0]["home"] +
                        item["statisticsItems"][0]["away"]
                    )

                # Ataques perigosos
                if name == "Dangerous attacks":
                    stats["dangerous_attacks"] = (
                        item["statisticsItems"][0]["home"] +
                        item["statisticsItems"][0]["away"]
                    )

    return stats


# ======================================================
# LÓGICA DE ANÁLISE — MODO 3 (AGRESSIVO)
# ======================================================
def analyze_game(event):
    minute = event.get("time", {}).get("minute")

    if not minute or minute < 12:
        return None

    home = event["homeTeam"]["name"]
    away = event["awayTeam"]["name"]

    event_id = event["id"]
    stats = get_stats(event_id)

    if not stats:
        return None

    shots_total = stats["shots_total"]
    shots_on = stats["shots_on_target"]
    corners = stats["corners"]
    dang = stats["dangerous_attacks"]

    # ----------------------------------------------
    # CÁLCULO DA PRESSÃO (modo agressivo)
    # ----------------------------------------------
    pressure = (shots_total * 2) + (shots_on * 3) + (corners * 2) + (dang / 5)

    # ENVIA ALERTA SE PRESSÃO ALTA
    if pressure >= 15:
        msg = f"""
🔥 <b>ALERTA OVER (Pressão Agressiva)</b>

🏟 <b>{home} x {away}</b>
⏱ Minuto: <b>{minute}</b>

🎯 Finalizações: <b>{shots_total}</b>
🥅 No alvo: <b>{shots_on}</b>
⛳ Escanteios: <b>{corners}</b>
⚡ Ataques perigosos: <b>{dang}</b>

🔥 Pressão: <b>{round(pressure, 1)}</b>

👉 Oportunidade de <b>OVER GOLS</b> detectada!
"""
        return msg

    return None


# ======================================================
# EXECUTAR ROBÔ EM LOOP
# ======================================================
def run_bot():
    already_sent = set()

    while True:
        print("🔄 Rodando... buscando jogos ao vivo.")
        games = get_live_games()

        print(f"📊 Jogos encontrados: {len(games)}")

        for event in games:
            try:
                home = event["homeTeam"]["name"]
                away = event["awayTeam"]["name"]
                print(f"⚽ Analisando: {home} x {away}")
            except:
                pass

            alert = analyze_game(event)

            if alert:
                event_id = event["id"]
                if event_id not in already_sent:
                    print("🚨 ALERTA ENVIADO!")
                    send_message(alert)
                    already_sent.add(event_id)

        print("⏳ Aguardando 60 segundos...\n")
        time.sleep(60)
# ======================================================================
# FLASK APENAS PARA HEALTHCHECK
# ======================================================================
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "BOT OVER GOLS RODANDO!"

# ======================================================
# INÍCIO
# ======================================================
if __name__ == "__main__":
    run_bot()
