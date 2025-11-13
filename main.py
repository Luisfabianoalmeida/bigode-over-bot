import requests
import time
import threading

TELEGRAM_TOKEN = "8544364550:AAGB37CwzJWVJt7DSafOH6DU28F9Wh2IgPA"
CHAT_ID = "6655882510"

# ======================================
# FUNÇÃO PARA ENVIAR MENSAGEM AO TELEGRAM
# ======================================
def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass


# ======================================
# PEGAR TODOS OS JOGOS AO VIVO DO SOFASCORE
# ======================================
def get_live_matches():
    try:
        url = "https://api.sofascore.com/api/v1/sport/football/events/live"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json().get("events", [])
        return []
    except:
        return []


# ======================================
# PEGAR ESTATÍSTICAS DO JOGO
# ======================================
def get_stats(match_id):
    try:
        url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None


# ======================================
# MONITORAMENTO COM PRESSÃO MODERADA
# ======================================
last_alert = {}  # guarda último alerta por jogo


def monitor():
    send_message("🤖 Robô OverGols Iniciado com Sucesso! Monitorando jogos ao vivo...")

    while True:
        matches = get_live_matches()

        for match in matches:

            match_id = match["id"]
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]
            league = match["tournament"]["name"]
            minute = match.get("time", {}).get("currentPeriodStartTimestamp", 0)

            score_home = match["homeScore"]["current"]
            score_away = match["awayScore"]["current"]

            stats = get_stats(match_id)
            if not stats:
                continue

            attacks_home = 0
            attacks_away = 0
            dangerous_home = 0
            dangerous_away = 0
            corners_home = 0
            corners_away = 0
            shots_home = 0
            shots_away = 0
            target_home = 0
            target_away = 0
            possession_home = 0
            possession_away = 0

            # --------------------------------------
            # PEGANDO TODAS AS ESTATÍSTICAS NECESSÁRIAS
            # --------------------------------------
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
                continue

            # SOMATÓRIOS
            total_attacks = dangerous_home + dangerous_away + attacks_home + attacks_away
            total_shots = shots_home + shots_away
            total_targets = target_home + target_away
            total_corners = corners_home + corners_away

            # -------------------------
            # GATILHOS DE PRESSÃO (MODERADO)
            # -------------------------
            if total_attacks >= 55 and total_shots >= 10 and total_targets >= 3 and total_corners >= 4:

                last = last_alert.get(match_id, 0)

                # evita spam extremo
                if time.time() - last >= 180:  # 3 minutos
                    last_alert[match_id] = time.time()

                    msg = f"""
💎 [Robô Over Gols - PREMIUM detectou uma chance quente!]

🏟 {league}
⚽️ {home} v {away}
🔢 Placar do jogo: {score_home} - {score_away}

📊 Dados do jogo (Mandante - Visitante):

- Investidas ofensivas: {attacks_home + dangerous_home} - {attacks_away + dangerous_away}
- Escanteios: {corners_home} - {corners_away}
- Arremates: {shots_home} - {shots_away}
- Tentativas no alvo: {target_home} - {target_away}
- Controle da bola: {possession_home} - {possession_away}

🔥 Sinal: Mais 1 gol na partida
                    """

                    send_message(msg)

        time.sleep(20)


# ======================================
# THREAD PRINCIPAL
# ======================================
def start():
    t = threading.Thread(target=monitor)
    t.daemon = True
    t.start()


if __name__ == "__main__":
    start()

    while True:
        time.sleep(60)
               
