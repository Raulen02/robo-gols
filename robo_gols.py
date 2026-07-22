import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

TOKEN = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
CHAT_ID = "519222308"

@app.route('/')
def home():
    return "Robo de Gols Avançado Rodando com Sucesso!"

def monitorar_jogos_ao_vivo():
    time.sleep(5)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload_inicio = {
        "chat_id": CHAT_ID, 
        "text": "🚨 *Robô de Gols com Métricas Avançadas (Pressão, xG e Janelas) Ativado!*", 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url_msg, json=payload_inicio)
    except Exception as e:
        print(f"Erro inicial: {e}")

    while True:
        try:
            pass
        except Exception as err:
            print(f"Erro no loop de monitoramento: {err}")
            
        time.sleep(60)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
