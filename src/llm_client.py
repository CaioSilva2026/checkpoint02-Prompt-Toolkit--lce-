import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")

if not OLLAMA_URL:
    raise EnvironmentError("OLLAMA_URL não encontrada. Crie um .env com OLLAMA_URL=http://localhost:11434")
if not MODEL:
    raise EnvironmentError("MODEL não encontrado. Crie um .env com MODEL=gpt-oss:120b")

def gerar_resposta(prompt: str, system: str = "", temperatura: float = 0.7) -> dict:

    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": system,
        "options": {"temperature": temperatura},
        "stream": False
    }

    inicio = time.time()
    response = requests.post(url, json=payload)
    tempo_ms = int((time.time() - inicio) * 1000)

    if response.status_code == 200:
        data = response.json()
        return {
            "resposta":        data.get("response", ""),
            "tokens_prompt":   data.get("prompt_eval_count", 0),
            "tokens_resposta": data.get("eval_count", 0),
            "tempo_ms":        tempo_ms
        }

    return {
        "resposta":        f"Erro: {response.status_code}",
        "tokens_prompt":   0,
        "tokens_resposta": 0,
        "tempo_ms":        tempo_ms
    }