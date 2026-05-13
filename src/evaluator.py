# 1. TOKENS — conta tokens usados na resposta
def avaliar_tokens(resposta: str) -> int:
    # Aproximação simples: 1 token ≈ 4 caracteres
    return len(resposta) // 4

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
def avaliar_temperatura(temperatura: float) -> dict:
    return {
        "temperatura": temperatura,
        "perfil": "determinístico" if temperatura == 0 else
                  "balanceado" if temperatura <= 0.7 else "criativo"
    }