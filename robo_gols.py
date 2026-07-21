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
    return "Robo de Gols rodando ativamente!"

def disparar_mensagem():
    # Aguarda o servidor estabilizar
    time.sleep(3)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": "🚨 *Robô de Gols Conectado e Operando com Sucesso!*", 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro: {e}")

# Inicia o envio em segundo plano assim que o aplicativo liga
thread = threading.Thread(target=disparar_mensagem)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
