import os
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"

@app.route('/')
def home():
    return "Robo de Gols rodando com sucesso!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "")
        
        # Se você mandar /start, ele responde e te confirma o Chat ID
        if texto == "/start":
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = {
                "chat_id": chat_id, 
                "text": f"🚨 *Robô Conectado com Sucesso!*\nSeu Chat ID é: `{chat_id}`", 
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload)
            
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
