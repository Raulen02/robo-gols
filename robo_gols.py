import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# Credenciais de conexão do Telegram
TOKEN = "8924431376:AAHTuD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
CHAT_ID = "519222308"

# Chave da RapidAPI (Sofascore)
RAPID_API_KEY = "79205a9d23msha37725343833c2ep114fc4jsn17b667a6327b"

@app.route('/')
def home():
    return "Robo de Gols (Modo Rua) Operacional! Acesse /testar para forcar um alerta no Telegram."

@app.route('/testar')
def testar_envio():
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url_msg, json={
            "chat_id": CHAT_ID, 
            "text": "🚨 *[TESTE MANUAL]* \nO robô está conectado e pronto para disparar os alertas na sua rua!", 
            "parse_mode": "Markdown"
        })
        if r.status_code == 200:
            return "Mensagem de teste enviada com sucesso para o Telegram!"
        else:
            return f"Erro ao enviar do Telegram: {r.text}"
    except Exception as e:
        return f"Erro: {e}"

def monitorar_jogos_ao_vivo():
    time.sleep(2)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    while True:
        try:
            url_api = "https://sofascore.p.rapidapi.com/matches/list-live"
            headers = {
                "X-RapidAPI-Key": RAPID_API_KEY,
                "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
            }
            
            resposta = requests.get(url_api, headers=headers, timeout=15)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                eventos = dados.get("events", [])
                
                for evento in eventos:
                    status_jogo = evento.get("status", {})
                    minuto = status_jogo.get("minute", 0)
                    
                    time_casa = evento.get("homeTeam", {}).get("name", "")
                    time_fora = evento.get("awayTeam", {}).get("name", "")
                    
                    tournament = evento.get("tournament", {})
                    nome_liga = tournament.get("name", "Campeonato Desconhecido")
                    categoria = tournament.get("category", {}).get("name", "")
                    liga_completa = f"{categoria} - {nome_liga}" if categoria else nome_liga
                    
                    placar_casa = evento.get("homeScore", {}).get("current", 0)
                    placar_fora = evento.get("awayScore", {}).get("current", 0)
                    gols_totais = placar_casa + placar_fora
                    
                    # 1º Tempo (HT) - 16' a 44' com jogo 0x0
                    if gols_totais == 0 and (16 <= minuto <= 44):
                        texto_alerta = (
                            f"🚨 *[ANTECIPADO] OVER 0.5 HT*\n\n"
                            f"🏆 *Liga:* {liga_completa}\n"
                            f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                            f"⏱ Minuto: {minuto}' | Placar: 0x0\n"
                            f"💡 *Aviso de Antecipação (Prepare-se para Odd 1.70+)*"
                        )
                        requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto_alerta, "parse_mode": "Markdown"})
                    
                    # 2º Tempo (FT) - 55' a 88' com até 2 gols totais
                    elif 0 <= gols_totais <= 2 and (55 <= minuto <= 88):
                        texto_alerta = (
                            f"🚨 *[ANTECIPADO] GOL LIMITE FT (0.5 / 1.5 / 2.5)*\n\n"
                            f"🏆 *Liga:* {liga_completa}\n"
                            f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                            f"⏱ Minuto: {minuto}' | Total de Gols: {gols_totais}\n"
                            f"💡 *Aviso de Antecipação (Prepare-se para Odd 1.70+)*"
                        )
                        requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto_alerta, "parse_mode": "Markdown"})
                        
        except Exception as err:
            print(f"Erro na varredura: {err}")
            
        time.sleep(45) # Reduzido para 45 segundos para varrer mais rápido

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
