import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")


def gerar_resposta(prompt):

    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()["response"]

    return f"Erro: {response.status_code}"