import os
from flask import Flask
import requests

app = Flask(__name__)

RAPID_API_KEY = "79205a9d23msha37725343833c2ep114fc4jsn17b667a6327b"
RAPID_API_HOST = "sofascore6.p.rapidapi.com"

@app.route('/')
def home():
    try:
        # Testando com a rota padrão correta da documentação do sofascore6
        url_api = "https://sofascore6.p.rapidapi.com/api/v1/sport/football/events/live"
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": RAPID_API_HOST
        }
        
        resposta = requests.get(url_api, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            eventos = dados.get("events", [])
            return f"API respondeu com Sucesso! (Status 200). Encontrados {len(eventos)} jogos ao vivo."
        else:
            return f"Erro da API: Status {resposta.status_code} - {resposta.text}"
            
    except Exception as e:
        return f"Erro crítico: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
