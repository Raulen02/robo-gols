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
    return "Robo de Gols (Lógica Pura & Estruturada) Operacional e Estável!"

@app.route('/testar')
def testar_envio():
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url_msg, json={
            "chat_id": CHAT_ID, 
            "text": "🧠 *[TESTE DE LÓGICA PURA]*\nDeploy corrigido com sucesso! O robô agora prioriza a estrutura: Critério Técnico -> Aba/Campo de Busca -> Alerta Prático.", 
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
    alerta_enviado = {}

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
                    match_id = evento.get("id")
                    status_jogo = evento.get("status", {})
                    
                    tipo_periodo = status_jogo.get("description", "") # "1st" ou "2nd"
                    minuto_bruto = status_jogo.get("minute", 0)
                    
                    # Ignorar acréscimos: trava estritamente no tempo regulamentar de 0 a 45 por tempo
                    if minuto_bruto > 45:
                        continue 
                        
                    minuto = minuto_bruto
                    minuto_total = minuto if tipo_periodo == "1st" else (45 + minuto)
                    
                    time_casa = evento.get("homeTeam", {}).get("name", "")
                    time_fora = evento.get("awayTeam", {}).get("name", "")
                    
                    tournament = evento.get("tournament", {})
                    nome_liga = tournament.get("name", "Campeonato")
                    categoria = tournament.get("category", {}).get("name", "")
                    liga_completa = f"{categoria} - {nome_liga}" if categoria else nome_liga
                    
                    placar_casa = evento.get("homeScore", {}).get("current", 0)
                    placar_fora = evento.get("awayScore", {}).get("current", 0)
                    gols_totais = placar_casa + placar_fora
                    
                    # -------------------------------------------------------------------------
                    # 1. 1º TEMPO (15' a 45' regulamentar | 0x0) -> Foco: Over 0.5 HT
                    # -------------------------------------------------------------------------
                    if tipo_periodo == "1st" and 15 <= minuto <= 45 and gols_totais == 0:
                        chave = f"{match_id}_1T_0.5HT"
                        if chave not in alerta_enviado:
                            texto = (
                                f"🧠 *ANÁLISE DE MERCADO: OVER 0.5 HT*\n\n"
                                f"🏆 *Campeonato:* {liga_completa}\n"
                                f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                                f"⏱ *Tempo Regulamentar:* {minuto_total}º min (1º Tempo)\n\n"
                                f"🔍 *1. O que procurar (Critério Técnico):*\n"
                                f"• Partida travada em 0x0 com pressão territorial contínua de um ou ambos os lados.\n\n"
                                f"📂 *2. Onde buscar (Abas / Campos do App):* \n"
                                f"• **Aba Estatísticas (Filtro 1º Tempo):** Conferir contagem de chutes no alvo, chutes bloqueados e ataques perigosos.\n"
                                f"• **Aba Odds:** Monitorar a cotação do mercado esticar na faixa ideal.\n\n"
                                f"🎯 *3. Resultado da Pesquisa / Alvo:* Entrada técnica recomendada no *Over 0.5 Gols no 1º Tempo*."
                            )
                            requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
                            alerta_enviado[chave] = True

                    # -------------------------------------------------------------------------
                    # 2. 2º TEMPO (10' a 45' regulamentar do 2T, total 55' a 90')
                    # -------------------------------------------------------------------------
                    elif tipo_periodo == "2nd" and 10 <= minuto <= 45:
                        
                        # Cenário A: Jogo 0x0 no segundo tempo
                        if gols_totais == 0:
                            chave = f"{match_id}_2T_0.5FT_0x0"
                            if chave not in alerta_enviado:
                                texto = (
                                    f"🧠 *ANÁLISE DE MERCADO: PRÓXIMO GOL / 0.5 FT*\n\n"
                                    f"🏆 *Campeonato:* {liga_completa}\n"
                                    f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                                    f"⏱ *Tempo Regulamentar:* {minuto_total}º min (2º Tempo)\n\n"
                                    f"🔍 *1. O que procurar (Critério Técnico):*\n"
                                    f"• Jogo zerado na etapa complementar com forte aceleração ofensiva e volume alto.\n\n"
                                    f"📂 *2. Onde buscar (Abas / Campos do App):*\n"
                                    f"• **Aba Estatísticas (Gráfico de Fluxo):** Analisar qual time está sufocando o adversário no campo de ataque.\n"
                                    f"• **Aba Odds:** Acompanhar o mercado de Próximo Gol para pegar cotações de valor.\n\n"
                                    f"🎯 *3. Resultado da Pesquisa / Alvo:* Buscar o primeiro gol da partida aproveitando o desequilíbrio defensivo."
                                )
                                requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
                                alerta_enviado[chave] = True

                        # Cenário B: Jogo 1x0 ou 0x1 (1 gol)
                        elif gols_totais == 1:
                            chave = f"{match_id}_2T_1.5FT_1gols"
                            if chave not in alerta_enviado:
                                texto = (
                                    f"🧠 *ANÁLISE DE MERCADO: OVER 1.5 FT*\n\n"
                                    f"🏆 *Campeonato:* {liga_completa}\n"
                                    f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                                    f"⏱ *Tempo Regulamentar:* {minuto_total}º min | Placar: {placar_casa}x{placar_fora}\n\n"
                                    f"🔍 *1. O que procurar (Critério Técnico):*\n"
                                    f"• Cenário de 1 gol onde a equipe perdedor se atira ao ataque, criando transições e espaços.\n\n"
                                    f"📂 *2. Onde buscar (Abas / Campos do App):*\n"
                                    f"• **Aba Estatísticas:** Checar entradas no terço final e finalizações de dentro da área.\n"
                                    f"• **Aba Odds:** Avaliar o mercado de Gols da Partida (Mais de 1.5).\n\n"
                                    f"🎯 *3. Resultado da Pesquisa / Alvo:* Entrada no *Over 1.5 Gols no Jogo* (precisa de apenas mais 1 gol)."
                                )
                                requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
                                alerta_enviado[chave] = True

                        # Cenário C: Jogo 1x1 ou 2x0 (2 gols)
                        elif gols_totais == 2:
                            chave = f"{match_id}_2T_2.5FT_2gols"
                            if chave not in alerta_enviado:
                                texto = (
                                    f"🧠 *ANÁLISE DE MERCADO: OVER 2.5 FT*\n\n"
                                    f"🏆 *Campeonato:* {liga_completa}\n"
                                    f"⚽ {time_casa} {placar_casa} x {placar_fora} {time_fora}\n"
                                    f"⏱ *Tempo Regulamentar:* {minuto_total}º min | Placar: {placar_casa}x{placar_fora}\n\n"
                                    f"🔍 *1. O que procurar (Critério Técnico):*\n"
                                    f"• Partida aberta, lá e cá, com alta frequência de finalizações de ambos os lados.\n\n"
                                    f"📂 *2. Onde buscar (Abas / Campos do App):*\n"
                                    f"• **Aba Estatísticas:** Validar constância de chutes ao gol e perigo real.\n"
                                    f"• **Aba Odds:** Olhar o mercado de Gols da Partida (Mais de 2.5).\n\n"
                                    f"🎯 *3. Resultado da Pesquisa / Alvo:* Entrada no *Over 2.5 Gols no Jogo* com alta probabilidade do 3º tento."
                                )
                                requests.post(url_msg, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"})
                                alarme_enviado = True # chave gravada
                                
        except Exception as err:
            print(f"Erro na varredura: {err}")
            
        time.sleep(30)

thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
