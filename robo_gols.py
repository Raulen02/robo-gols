import os
from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

TOKEN = "COLE_O_SEU_TOKEN_AQUI"
CHAT_ID = "519222308"

@app.route('/')
def home():
    return "Robo de Gols Avançado Rodando com Sucesso!"

def monitorar_jogos_ao_vivo():
    # Aguarda o servidor estabilizar no Render
    time.sleep(5)
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Mensagem inicial indicando que o cérebro do robô ligou
    payload_inicio = {
        "chat_id": CHAT_ID, 
        "text": "🚨 *Robô de Gols com Métricas Avançadas (Pressão, xG e Janelas) Ativado!*", 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url_msg, json=payload_inicio)
    except Exception as e:
        print(f"Erro inicial: {e}")

    # Loop contínuo de varredura
    while True:
        try:
            # ==========================================
            # AQUI ENTRARÁ A SUA API DE DADOS DE FUTEBOL
            # ==========================================
            # O robô varre os jogos em andamento. Quando uma partida 
            # atinge os critérios (Ex: Minuto 15-42 ou 60-88, com xG subindo, 
            # pressão e finalizações ativas), ele dispara o alerta abaixo:
            
            # Exemplo de disparo estruturado para o seu Telegram:
            # alerta_texto = "🔥 *OPORTUNIDADE DE GOL!*\n⚽ *Jogo:* Time A x Time B\n⏱ *Minuto:* 78'\n📊 *Pressão/xG:* Altíssima"
            # requests.post(url_msg, json={"chat_id": CHAT_ID, "text": alerta_texto, "parse_mode": "Markdown"})
            
            pass # Mantém o loop rodando sem sobrecarregar o servidor
            
        except Exception as err:
            print(f"Erro no loop de monitoramento: {err})
            
        # Pausa de 60 segundos entre cada varredura global para poupar recursos
        time.sleep(60)

# Inicia a varredura em segundo plano junto com o Flask
thread = threading.Thread(target=monitorar_jogos_ao_vivo)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
