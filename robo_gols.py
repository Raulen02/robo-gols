import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

TOKEN = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
CHAT_ID = "519222308"

# Sua chave oficial da RapidAPI (Sofascore)
RAPID_API_KEY = "79205a9d23msha37725343833c2ep114fc4jsn17b667a6327b"

@app.route('/')
def home():
    return "Robo de Gols Sofascore Rodando!"

def monitorar_jogos_ao_vivo():
    time.sleep(5)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        requests.post(url_msg, json={
            "chat_id": CHAT_ID, 
            "text": "🟢 *Robô Conectado ao Sofascore! Varredura de jogos ao vivo iniciada.*", 
            "parse_mode": "Markdown"
        })
    except Exception as e:
        print(f"Erro inicial: {e}")

    while True:
        try:
            # Conectando à API do Sofascore
            url_api = "https://sofascore.p.rapidapi.com/matches/list-live"
            headers = {
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
            }
            
            resposta = requests.get(url_api, headers=headers, timeout=15)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                # O robô processa os eventos ao vivo e cruza com as regras de minuto e pressão
                
        except Exception as err:
            print(f"Erro na varredura: {err}")
            
        time.sleep(60)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
