import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

TOKEN = "8924431376:AAHTuD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
CHAT_ID = "519222308"

# Chave oficial atualizada e vinculada ao seu plano da RapidAPI
RAPID_API_KEY = "79205a9d23msha37725343833c2ep114fc4jsn17b667a6327b"
RAPID_API_HOST = "sofascore6.p.rapidapi.com"

@app.route('/')
def home():
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        url_api = "https://sofascore6.p.rapidapi.com/api/sofascore/v1/sport/football/events/live"
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": RAPID_API_HOST
        }
        
        resposta = requests.get(url_api, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            eventos = dados.get("events", [])
            
            if len(eventos) > 0:
                primeiro = eventos[0]
                t_casa = primeiro.get("homeTeam", {}).get("name", "Casa")
                t_fora = primeiro.get("awayTeam", {}).get("name", "Fora")
                
                texto = f"⚽ *Partida Ao Vivo:* {t_casa} x {t_fora}"
                requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
                return f"Sucesso total! Encontrados {len(eventos)} jogos ao vivo. O primeiro jogo ({t_casa} x {t_fora}) foi enviado para o Telegram!"
            else:
                return "API conectou perfeitamente (Status 200), mas não há jogos ao vivo no momento."
        else:
            return f"Erro retornado pela API: Status {resposta.status_code} - {resposta.text}"
            
    except Exception as e:
        return f"Erro crítico ao tentar ler a API: {e}"

def monitorar_jogos_ao_vivo():
    time.sleep(3)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    while True:
        try:
            url_api = "https://sofascore6.p.rapidapi.com/api/sofascore/v1/sport/football/events/live"
            headers = {
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": RAPID_API_HOST
            }
            
            resposta = requests.get(url_api, headers=headers, timeout=15)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                eventos = dados.get("events", [])
                
                if len(eventos) > 0:
                    primeiro = eventos[0]
                    t_casa = primeiro.get("homeTeam", {}).get("name", "Casa")
                    t_fora = primeiro.get("awayTeam", {}).get("name", "Fora")
                    
                    texto = f"⚽ *Partida Ao Vivo:* {t_casa} x {t_fora}"
                    requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
        except Exception:
            pass
            
        time.sleep(30)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
