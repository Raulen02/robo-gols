import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# Credenciais do Telegram validadas
TOKEN = "8924431376:AAHTuD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
CHAT_ID = "519222308"

# Chave da RapidAPI (Sofascore)
RAPID_API_KEY = "79205a9d23msha37725343833c2ep114fc4jsn17b667a6327b"

@app.route('/')
def home():
    return "Robo em Teste Básico de Conexão!"

@app.route('/testar')
def testar_envio():
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url_msg, json={
            "chat_id": CHAT_ID, 
            "text": "🟢 *[TESTE BÁSICO]* Servidor do Render online e pronto para o teste de captura!", 
            "parse_mode": "Markdown"
        })
        if r.status_code == 200:
            return "Mensagem de teste enviada com sucesso!"
        else:
            return f"Erro: {r.text}"
    except Exception as e:
        return f"Erro: {e}"

def monitorar_jogos_ao_vivo():
    time.sleep(5)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    ja_enviado = set()

    while True:
        try:
            url_api = "https://sofascore.p.rapidapi.com/matches/list-live"
            headers = {
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
            }
            
            print("Consultando API do Sofascore...")
            resposta = requests.get(url_api, headers=headers, timeout=15)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                eventos = dados.get("events", [])
                print(f"Jogos encontrados na API: {len(eventos)}")
                
                # Pega os primeiros 3 jogos da lista apenas para testar se a informação flui
                contador = 0
                for evento in eventos:
                    match_id = evento.get("id")
                    
                    if match_id in ja_enviado:
                        continue
                        
                    time_casa = evento.get("homeTeam", {}).get("name", "Casa")
                    time_fora = evento.get("awayTeam", {}).get("name", "Fora")
                    
                    status_jogo = evento.get("status", {})
                    minuto = status_jogo.get("minute", 0)
                    periodo = status_jogo.get("description", "Ao Vivo")
                    
                    placar_casa = evento.get("homeScore", {}).get("current", 0)
                    placar_fora = evento.get("awayScore", {}).get("current", 0)
                    
                    # Monta o alerta cru para testar a captura
                    texto = (
                        f"🚨 *TESTE DE CAPTURA DO SOFASCORE*\n\n"
                        f"⚽ *{time_casa} {placar_casa} x {placar_fora} {time_fora}*\n"
                        f"⏱ Status/Minuto: {minuto}' ({periodo})\n"
                        f"🆔 ID da Partida: {match_id}"
                    )
                    
                    requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
                    ja_enviado.add(match_id)
                    
                    contador += 1
                    if contador >= 2:  # Envia no máximo 2 para não lotar o chat de uma vez só
                        break
            else:
                print(f"Erro na resposta da API Sofascore: {resposta.status_code} - {resposta.text}")
                
        except Exception as err:
            print(f"Erro crítico no loop de captura: {err}")
            
        # Espera 60 segundos para o próximo ciclo de teste
        time.sleep(60)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
