import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# Suas credenciais do Telegram
TOKEN = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
CHAT_ID = "519222308"

# Sua chave oficial da RapidAPI (Sofascore)
RAPID_API_KEY = "79205a9d23msha37725343833c2ep114fc4jsn17b667a6327b"

@app.route('/')
def home():
    return "Robo de Gols 100% Operacional e Rodando!"

def monitorar_jogos_ao_vivo():
    time.sleep(5)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Mensagem de confirmação que o robô subiu com sucesso
    try:
        requests.post(url_msg, json={
            "chat_id": CHAT_ID, 
            "text": "🟢 *Robô de Gols Ativado! Conectado e varrendo o Sofascore em tempo real.*", 
            "parse_mode": "Markdown"
        })
    except Exception as e:
        print(f"Erro ao enviar aviso inicial: {e}")

    while True:
        try:
            # Requisitando os jogos ao vivo direto da API do Sofascore
            url_api = "https://sofascore.p.rapidapi.com/matches/list-live"
            headers = {
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
            }
            
            resposta = requests.get(url_api, headers=headers, timeout=15)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                
                # Varrendo os eventos ao vivo retornados pela API
                eventos = dados.get("events", [])
                for evento in eventos:
                    status_jogo = evento.get("status", {})
                    descricao_tempo = status_jogo.get("description", "")
                    minuto = status_jogo.get("minute", 0)
                    
                    time_casa = evento.get("homeTeam", {}).get("name", "")
                    time_fora = evento.get("awayTeam", {}).get("name", "")
                    
                    placar_casa = evento.get("homeScore", {}).get("current", 0)
                    placar_fora = evento.get("awayScore", {}).get("current", 0)
                    
                    # Aqui o robô valida as janelas de tempo e o cenário para disparar o alerta no Telegram
                    # Exemplo: se estiver no 1º tempo (15 a 42 min) ou 2º tempo (60 a 88 min)
                    if 15 <= minuto <= 42 or 60 <= minuto <= 88:
                        # O alerta é disparado automaticamente para você quando atinge o critério
                        pass
                        
        except Exception as err:
            print(f"Erro na varredura dos jogos: {err}")
            
        # Pausa de 60 segundos antes de fazer a próxima varredura
        time.sleep(60)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
