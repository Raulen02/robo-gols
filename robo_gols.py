import requests

token = "8924431376:AAHtUD9kI_gQRTTFSzRSZvtii8uX9cM-qF4"
chat_id = "519222308"
url = f"https://api.telegram.org/bot{token}/sendMessage"

mensagem = "Robo Conectado com Sucesso no Render!"
payload = {"chat_id": chat_id, "text": mensagem}

resposta = requests.post(url, json=payload)
print(resposta.json())
