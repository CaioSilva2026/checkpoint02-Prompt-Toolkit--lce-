# 1. TOKENS — conta tokens usados na resposta
import tiktoken

def avaliar_tokens(texto: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(texto))

# 2. ACURÁCIA — compara output com gabarito (para classificação)
def avaliar_acuracia(output: str, gabarito: str) -> float:
    return 1.0 if output.strip().upper() == gabarito.strip().upper() else 0.0

# 3. CONSISTÊNCIA — roda o mesmo input N vezes e mede variação
def avaliar_consistencia(outputs: list[str]) -> float:
    # Retorna % de vezes que a resposta foi igual à mais comum
    from collections import Counter
    if not outputs:
        return 0.0
    mais_comum = Counter(outputs).most_common(1)[0][1]
    return mais_comum / len(outputs)

# 4. TEMPERATURA — registra a temperatura usada na chamada
def testar_temperatura(prompt: str, gerar_resposta_fn, temps: list = [0.1, 0.5, 1.0]) -> list:

    resultados = []
    for temp in temps:
        resultado = gerar_resposta_fn(prompt=prompt, temperatura=temp)
        resultado["temperatura"] = temp
        resultados.append(resultado)
    return resultados