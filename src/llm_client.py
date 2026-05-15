from ollama import Client
import os
import time
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

if not OLLAMA_API_KEY:
    raise EnvironmentError(
        "OLLAMA_API_KEY não encontrada. "
        "Crie um .env com OLLAMA_API_KEY=sua_chave_aqui"
    )

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + OLLAMA_API_KEY}
)

def gerar_resposta(prompt: str, system: str = "", temperatura: float = 0.7) -> dict:

    mensagens = []

    if system and system.strip():
        mensagens.append({"role": "system", "content": system})

    mensagens.append({"role": "user", "content": prompt})

    inicio = time.time()

    try:
        resposta = client.chat(
            model="gpt-oss:120b",
            messages=mensagens,
            options={"num_predict": 300, "temperature": temperatura},
            stream=False
        )
        tempo_ms = int((time.time() - inicio) * 1000)

        conteudo = resposta["message"]["content"].strip()

        return {
            "resposta":        conteudo,
            "tokens_prompt":   resposta.get("prompt_eval_count", 0),
            "tokens_resposta": resposta.get("eval_count", 0),
            "tempo_ms":        tempo_ms
        }

    except Exception as e:
        tempo_ms = int((time.time() - inicio) * 1000)
        return {
            "resposta":        f"Erro: {e}",
            "tokens_prompt":   0,
            "tokens_resposta": 0,
            "tempo_ms":        tempo_ms
        }

