import requests
import time
import threading

TELEGRAM_TOKEN = "8544364550:AAGB37CwzJWVJt7DSafOH6DU28F9Wh2IgPA"
CHAT_ID = "6655882510"

MATCH_ID = 15016652  # Angola x Argentina

# ================================
# ENVIO PARA TELEGRAM
# ================================
def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass


# ================================
# ESTATÍSTICAS DO JOGO
# ================================
def get_stats(match_id):
    try:
        url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None


# ================================
# INFORMAÇÕES DO JOGO (PLACAR, MINUTO, TIMES)
# ================================
def get_event_info(match_id):
    try:
        url = f"https://api.sofascore.com/api/v1/event/{match_id}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()["event"]
        return None
    except:
        return None


# ================================
# MONITORAMENTO EXCLUSIVO DO JOGO
# ================================
last_alert = {}

def monitor():
    send_message("🤖 Robô OverGols ligado! Monitorando Angola x Argentina...")

    while True:
        event = get_event_info(MATCH_ID)
        if not event:
            time.sleep(10)
            continue
        
        home = event["homeTeam"]["name"]
        away = event["awayTeam"]["name"]
        league = event["tournament"]["name"]

        score_home = event["homeScore"]["current"]
        score_away = event["awayScore"]["current"]

        minute = event.get("time", {}).get("currentPeriodStartTimestamp", 0)

        stats = get_stats(MATCH_ID)
        if not stats:
            time.sleep(10)
            continue

        # =======================================
        # VARIÁVEIS DAS ESTATÍSTICAS
        # =======================================
        attacks_home = attacks_away = 0
        dangerous_home = dangerous_away = 0
        corners_home = corners_away = 0
        shots_home = shots_away = 0
        target_home = target_away = 0
        possession_home = possession_away = 0

        try:
            groups = stats["statistics"][0]["groups"]
            for group in groups:
                for item in group["statisticsItems"]:
                    name = item["name"]

                    if name == "Attacks":
                        attacks_home = item["home"]
                        attacks_away = item["away"]

                    if name == "Dangerous Attacks":
                        dangerous_home = item["home"]
                        dangerous_away = item["away"]

                    if name == "Corner kicks":
                        corners_home = item["home"]
                        corners_away = item["away"]

                    if name == "Shots":
                        shots_home = item["home"]
                        shots_away = item["away"]

                    if name == "Shots on target":
                        target_home = item["home"]
                        target_away = item["away"]

                    if name == "Ball possession":
                        possession_home = item["home"]
                        possession_away = item["away"]

        except:
            time.sleep(10)
            continue

        total_attacks = (
            attacks_home + dangerous_home +
            attacks_away + dangerous_away
        )
        total_shots = shots_home + shots_away
        total_targets = target_home + target_away
        total_corners = corners_home + corners_away

        # =======================================
        # GATILHOS - PRESSÃO CONSIDERÁVEL
        # =======================================
        if (
            total_attacks >= 20 and
            total_shots >= 8 and
            total_targets >= 2 and
            total_corners >= 3 and
            minute >= 35
        ):

            last = last_alert.get(MATCH_ID, 0)

            # Evita spam total — mínimo 2 minutos entre sinais
            if time.time() - last >= 120:
                last_alert[MATCH_ID] = time.time()

                msg = f"""
💎 [Robô Over Gols — Oportunidade Detectada!]

🏟 {league}
⚽️ {home} x {away}
🕐 Minuto: {minute}
🔢 Placar: {score_home} - {score_away}

📊 Dados do jogo (Mandante - Visitante):

- Investidas ofensivas: {attacks_home + dangerous_home} - {attacks_away + dangerous_away}
- Escanteios: {corners_home} - {corners_away}
- Arremates: {shots_home} - {shots_away}
- Chutes no alvo: {target_home} - {target_away}
- Posse de bola: {possession_home} - {possession_away}

🔥 Sinal: Mais 1 gol na partida!
"""

                send_message(msg)

        time.sleep(12)


# ================================
# THREAD
# ================================
def start():
    t = threading.Thread(target=monitor)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    start()
    while True:
        time.sleep(60)
               
