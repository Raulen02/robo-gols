import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# Credenciais de conexão do Telegram
TOKEN = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
CHAT_ID = "519222308"

# Chave da RapidAPI (Sofascore)
RAPID_API_KEY = "79205a9d23msha37725343833c2ep114fc4jsn17b667a6327b"

@app.route('/')
def home():
    return "Robo de Gols Limite (Especialista Odds 1.70+) Operacional!"

def monitorar_jogos_ao_vivo():
    time.sleep(5)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Mensagem de inicialização confirmando o foco em Gols Limite e Odds 1.70+
    try:
        requests.post(url_msg, json={
            "chat_id": CHAT_ID, 
            "text": "🟢 *Robô de Gols Limite Ativado!*\n🎯 *Estratégia:* Prioridade Absoluta em **0.5 HT** (20'-44') + **Gol Limite 0.5 e 1.5 FT** (60'-88') com Odd Mínima de 1.70.", 
            "parse_mode": "Markdown"
        })
    except Exception as e:
        print(f"Erro inicial: {e}")

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
                    
                    placar_casa = evento.get("homeScore", {}).get("current", 0)
                    placar_fora = evento.get("awayScore", {}).get("current", 0)
                    gols_totais = placar_casa + placar_fora
                    
                    # =========================================================================
                    # 🥇 PRIORIDADE MÁXIMA 1: GOL LIMITE 0.5 HT (PRIMEIRO TEMPO - 20' a 44')
                    # =========================================================================
                    # Foco total na sua maior fonte de lucro com odds esticadas (1.70+)
                    if gols_totais == 0 and (20 <= minuto <= 44):
                        texto_alerta = (
                            f"🚨 *ALERTA MESTRE: GOL LIMITE 0.5 HT* 💰\n\n"
                            f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                            f"⏱ Minuto: {minuto}' (Odd Mínima Alvo: 1.70+)\n"
                            f"💡 *Critério:* Jogo 0x0 na janela de ouro do primeiro tempo, buscando o gol antes do intervalo!"
                        )
                        requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto_alerta, "parse_mode": "Markdown"})
                    
                    # =========================================================================
                    # 🎯 PRIORIDADE MÁXIMA 2: GOL LIMITE 0.5 FT (SEGUNDO TEMPO - 60' a 88')
                    # =========================================================================
                    elif gols_totais == 0 and (60 <= minuto <= 88):
                        texto_alerta = (
                            f"🎯 *ALERTA: GOL LIMITE 0.5 FT (2º Tempo)* 📊\n\n"
                            f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                            f"⏱ Minuto: {minuto}' (Odd Mínima Alvo: 1.70+)\n"
                            f"💡 *Critério:* Jogo 0x0 na reta final, monitorando o comportamento para o gol limite!"
                        )
                        requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto_alerta, "parse_mode": "Markdown"})
                    
                    # =========================================================================
                    # ⚡ PRIORIDADE MÁXIMA 3: GOL LIMITE 1.5 FT (SEGUNDO TEMPO - 60' a 88')
                    # =========================================================================
                    elif gols_totais == 1 and (60 <= minuto <= 88):
                        texto_alerta = (
                            f"⚡ *ALERTA: GOL LIMITE 1.5 FT (Busca do 2º Gol)* 🚀\n\n"
                            f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                            f"⏱ Minuto: {minuto}' (Odd Mínima Alvo: 1.70+)\n"
                            f"💡 *Critério:* Partida com 1 gol, fluxo aberto a partir dos 60' em busca do segundo tento."
                        )
                        requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto_alerta, "parse_mode": "Markdown"})
                        
        except Exception as err:
            print(f"Erro na varredura: {err}")
            
        time.sleep(60)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
