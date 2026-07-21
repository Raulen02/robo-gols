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

def loop_envio():
    # Dá um tempo para o servidor web subir completamente
    time.sleep(5)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Envia uma mensagem inicial avisando que o robô conectou de vez
    payload = {
        "chat_id": CHAT_ID, 
        "text": "🚨 *Robô de Gols Conectado e Operando com Sucesso!*", 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar: {e}")

# Inicia a thread em segundo plano para mandar a mensagem sem derrubar o site do Render
thread = threading.Thread(target=loop_envio)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
