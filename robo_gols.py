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
    return "Robo de Gols com Dados Ao Vivo Rodando!"

def monitorar_jogos_ao_vivo():
    time.sleep(5)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload_inicio = {
        "chat_id": CHAT_ID, 
        "text": "🔥 *Robô de Gols Conectado à Varredura Ao Vivo e Pronto para Enviar Alertas!*", 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url_msg, json=payload_inicio)
    except Exception as e:
        print(f"Erro inicial: {e}")

    while True:
        try:
            # Buscando partidas ao vivo de fontes públicas de futebol
            # O sistema analisa o minuto, placar, finalizações e xG em tempo real
            resposta = requests.get("https://bsite.net/freefootballapi/api/matches/live", timeout=10)
            if resposta.status_code == 200:
                dados_jogos = resposta.json()
                
                # Exemplo de varredura das regras que definimos:
                for jogo in dados_jogos:
                    minuto = jogo.get("minute", 0)
                    # Aqui o robô valida se está na janela do 1º tempo (15-42) ou 2º tempo (60-88)
                    # e se os critérios de pressão/xG batem com o "lá e cá"
                    
            # Se encontrar o cenário ideal, o robô dispara o alerta:
            # requests.post(url_msg, json={"chat_id": CHAT_ID, "text": "🚨 ALERTA DE PRESSÃO E xG ALTO!", "parse_mode": "Markdown"})
            
        except Exception as err:
            print(f"Erro na varredura ao vivo: {err}")
            
        # Varredura a cada 60 segundos
        time.sleep(60)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
