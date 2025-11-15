import requests
import time
from datetime import datetime
import threading

# ==========================
# CONFIGURAÇÕES DO ROBÔ
# ==========================

TELEGRAM_TOKEN = "8544364550:AAGB37CwzJWVJt7DSafOH6DU28F9Wh2IgPA"
CHAT_ID = "6655882510"

# ID DO JOGO QUE VOCÊ QUER MONITORAR
# Exemplo: Argentina x Angola → id 15016652
MATCH_ID = "15016652"

# Frequência de checagem (em segundos)
CHECK_INTERVAL = 30

# Regras para enviar sinal
MIN_TOTAL_SHOTS = 5         # chutes no gol somados
MIN_TOTAL_ATTACKS = 20      # ataques perigosos somados
PRESSURE_DELTA = 8          # diferença de pressão

# ==========================
# FUNÇÕES DE OPERAÇÃO
# ==========================

def send_message(text):
    """Envia mensagem para o Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)


def get_match_stats(match_id):
    """Busca estatísticas reais do SofaScore."""
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    stats = {
        "shots_home": 0,
        "shots_away": 0,
        "dangerous_attacks_home": 0,
        "dangerous_attacks_away": 0
    }

    # Varre todas as estatísticas
    for group in data.get("statistics", []):
        for item in group.get("statisticsItems", []):
            name = item.get("name")
            home = item.get("home", 0)
            away = item.get("away", 0)

            if name == "Shots on target":
                stats["shots_home"] = home
                stats["shots_away"] = away

            if name == "Dangerous attacks":
                stats["dangerous_attacks_home"] = home
                stats["dangerous_attacks_away"] = away

    return stats


def analyze_and_send():
    """Analisa estatísticas e envia sinal quando os critérios batem."""

    send_message("🤖 Robô OverGols iniciado! Monitorando estatísticas em tempo real...")

    while True:
        stats = get_match_stats(MATCH_ID)

        if not stats:
            print("Erro ao puxar estatísticas...")
            time.sleep(CHECK_INTERVAL)
            continue

        home_shots = stats["shots_home"]
        away_shots = stats["shots_away"]
        total_shots = home_shots + away_shots

        home_da = stats["dangerous_attacks_home"]
        away_da = stats["dangerous_attacks_away"]
        total_attacks = home_da + away_da

        pressure_diff = abs(home_da - away_da)

        # CRITÉRIO PARA ENVIAR SINAL
        if total_shots >= MIN_TOTAL_SHOTS and total_attacks >= MIN_TOTAL_ATTACKS:

            press_team = "Casa" if home_da > away_da else "Fora"

            msg = (
                "🔥 *SINAL DE OVER GOLS DETECTADO!*\n\n"
                f"Chutes no gol: {total_shots}\n"
                f"Ataques perigosos: {total_attacks}\n"
                f"Time pressionando: *{press_team}*\n"
                "\n⚽ Possível entrada em *OVER GOLS*"
            )

            send_message(msg)

        time.sleep(CHECK_INTERVAL)


def start_bot():
    thread = threading.Thread(target=analyze_and_send)
    thread.daemon = True
    thread.start()


# ==========================
# INICIAR ROBÔ
# ==========================

if __name__ == "__main__":
    start_bot()

    # Mantém rodando no Render
    while True:
        time.sleep(60)
               
