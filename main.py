requests
import time

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

                if name == "Total shots":
                    stats["shots_total"] = (
                        item["statisticsItems"][0]["home"] +
                        item["statisticsItems"][0]["away"]
                    )

                if name == "Shots on target":
                    stats["shots_on_target"] = (
                        item["statisticsItems"][0]["home"] +
                        item["statisticsItems"][0]["away"]
                    )

                if name == "Corner kicks":
                    stats["corners"] = (
                        item["statisticsItems"][0]["home"] +
                        item["statisticsItems"][0]["away"]
                    )

                if name == "Dangerous attacks":
                    stats["dangerous_attacks"] = (
                        
