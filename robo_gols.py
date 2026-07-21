import time
import requests

token = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
chat_id = "519222308"
url = f"https://api.telegram.org/bot{token}/sendMessage"

contador = 0

while True:
    contador += 1
    mensagem = f"Teste de conexao numero {contador}"
    payload = {"chat_id": chat_id, "text": mensagem}
    
    resposta = requests.post(url, json=payload)
    print("Resposta do Telegram:", resposta.json())
    
    # Espera 30 segundos antes de enviar a próxima
    time.sleep(30)
