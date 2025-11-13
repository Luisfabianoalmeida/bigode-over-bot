import requests
import time
import threading

# ======================================
# CONFIGURAÇÕES DO BOT
# ======================================
TELEGRAM_TOKEN = "8544364550:AAGB37CwzJWVJt7DSafOH6DU28F9Wh2IgPA"
CHAT_ID = "6655882510"

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}

    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)


# ======================================
# PEGAR ESTATÍSTICAS DOS JOGOS
# ======================================
def get_match_stats(match_id):
    try:
        url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()

        return None

    except Exception as e:
        print("Erro ao buscar dados:", e)
        return None


# ======================================
# LÓGICA DO ROBÔ
# ALERTA QUANDO TIVER 5 CHUTES SOMADOS
# ======================================
def monitor_games():

    # IDs de teste (trocar depois pelos reais)
    MATCHES = [123456, 789101]

    send_message("🤖 Robô OverGols iniciado com sucesso!")

    while True:
        for match_id in MATCHES:
            data = get_match_stats(match_id)

            if not data:
                continue

            total_shots = 0

            try:
                stats = data["statistics"][0]["groups"]

                for group in stats:
                    for item in group["statisticsItems"]:
                        if item["name"] == "Shots on target":
                            total_shots += item["home"]
                            total_shots += item["away"]

            except:
                pass

            if total_shots >= 5:
                send_message(
                    f"🔥 Pressão detectada!\n"
                    f"Jogo ID: {match_id}\n"
                    f"Chutes no gol: {total_shots}"
                )

        time.sleep(30)


# ======================================
# THREAD PARA O LOOP RODAR NO RENDER
# ======================================
def start_thread():
    t = threading.Thread(target=monitor_games)
    t.daemon = True
    t.start()


# ======================================
# INÍCIO DO PROGRAMA
# ======================================
if __name__ == "__main__":
    start_thread()

    # Mantém o app vivo no Render
    while True:
        time.sleep(60)

               
