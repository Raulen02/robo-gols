import time
import requests

token = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
chat_id = "519222308"
url = f"https://api.telegram.org/bot{token}/sendMessage"

# Mensagem inicial de aviso
payload = {"chat_id": chat_id, "text": "Robo de Gols Ativo e Monitorando!"}
requests.post(url, json=payload)

# Mantém o aplicativo rodando para o Render não desligar
while True:
    print("Robo rodando...")
    time.sleep(60)
