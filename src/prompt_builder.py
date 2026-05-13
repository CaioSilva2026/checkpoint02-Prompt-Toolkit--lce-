"""
prompt_builder.py
Módulo responsável pela montagem e estruturação de prompts.
Separa instrução de dados e oferece utilitários para few-shot e CoT.
Referência: Aula 05 — Anatomia do Prompt
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Constantes de formatação
# ---------------------------------------------------------------------------

SEPARADOR = "\n" + "-" * 60 + "\n"


# ---------------------------------------------------------------------------
# Funções principais
# ---------------------------------------------------------------------------

def montar_prompt(
    instrucao: str,
    input_dados: str,
    contexto: Optional[str] = None,
    formato_output: Optional[str] = None,
) -> str:
    """
    Monta um prompt estruturado separando instrução de dados (Aula 05).

    Parâmetros
    ----------
    instrucao : str
        O que o modelo deve fazer. Deve ser clara e imperativa.
    input_dados : str
        O texto/dado sobre o qual o modelo vai operar.
    contexto : str, opcional
        Informações de contexto ou restrições adicionais.
    formato_output : str, opcional
        Especificação de como o modelo deve formatar a resposta.

    Retorna
    -------
    str
        Prompt completo pronto para envio ao LLM.

    Raises
    ------
    ValueError
        Se instrucao ou input_dados estiverem vazios.
    """
    _validar_nao_vazio(instrucao, "instrucao")
    _validar_nao_vazio(input_dados, "input_dados")

    partes = []

    # 1. Instrução (obrigatória)
    partes.append(f"### INSTRUÇÃO\n{instrucao.strip()}")

    # 2. Contexto (opcional)
    if contexto and contexto.strip():
        partes.append(f"### CONTEXTO\n{contexto.strip()}")

    # 3. Dado de entrada (obrigatório — separado da instrução)
    partes.append(f"### ENTRADA\n{input_dados.strip()}")

    # 4. Formato de saída (opcional, mas recomendado)
    if formato_output and formato_output.strip():
        partes.append(f"### FORMATO DE RESPOSTA\n{formato_output.strip()}")

    return SEPARADOR.join(partes)


def adicionar_exemplos(prompt: str, exemplos: list[dict]) -> str:
    """
    Injeta exemplos de few-shot em um prompt já montado.

    Os exemplos são inseridos logo antes da seção '### ENTRADA' para que
    o modelo os veja antes de processar o input real.

    Parâmetros
    ----------
    prompt : str
        Prompt base gerado por montar_prompt().
    exemplos : list[dict]
        Lista de dicts com chaves 'input' e 'output'.
        Exemplo: [{"input": "Adorei!", "output": "POSITIVO"}, ...]

    Retorna
    -------
    str
        Prompt com os exemplos inseridos.

    Raises
    ------
    ValueError
        Se o prompt não contiver a seção '### ENTRADA' ou se algum
        exemplo estiver malformado.
    """
    _validar_nao_vazio(prompt, "prompt")

    if not exemplos:
        return prompt

    _validar_exemplos(exemplos)

    # Formata bloco de exemplos
    linhas_exemplos = ["### EXEMPLOS (few-shot)"]
    for i, ex in enumerate(exemplos, start=1):
        linhas_exemplos.append(
            f"Exemplo {i}:\n"
            f"  Entrada : {str(ex['input']).strip()}\n"
            f"  Saída   : {str(ex['output']).strip()}"
        )
    bloco_exemplos = "\n\n".join(linhas_exemplos)

    # Insere antes de '### ENTRADA'
    marcador = "### ENTRADA"
    if marcador not in prompt:
        raise ValueError(
            "O prompt não contém a seção '### ENTRADA'. "
            "Use montar_prompt() para criar o prompt base."
        )

    return prompt.replace(marcador, f"{bloco_exemplos}{SEPARADOR}{marcador}", 1)


def adicionar_cot(prompt: str, passos: list[str]) -> str:
    """
    Adiciona instrução de Chain-of-Thought (raciocínio explícito) ao prompt.

    Os passos de raciocínio são anexados após a seção '### INSTRUÇÃO',
    orientando o modelo a pensar passo a passo antes de responder.

    Parâmetros
    ----------
    prompt : str
        Prompt base gerado por montar_prompt().
    passos : list[str]
        Lista de passos de raciocínio que o modelo deve seguir.
        Exemplo: ["Identifique aspectos positivos", "Compare e classifique"]

    Retorna
    -------
    str
        Prompt com as instruções de CoT inseridas.

    Raises
    ------
    ValueError
        Se o prompt não contiver '### INSTRUÇÃO' ou a lista de passos
        estiver vazia.
    """
    _validar_nao_vazio(prompt, "prompt")

    if not passos:
        return prompt

    if not isinstance(passos, list) or not all(isinstance(p, str) for p in passos):
        raise ValueError("'passos' deve ser uma lista de strings.")

    passos_formatados = "\n".join(
        f"  {i}. {passo.strip()}" for i, passo in enumerate(passos, start=1)
    )
    bloco_cot = (
        "Antes de responder, raciocine explicitamente seguindo estes passos:\n"
        f"{passos_formatados}\n\n"
        "Após o raciocínio, forneça a resposta final no formato solicitado."
    )

    marcador = "### INSTRUÇÃO\n"
    if marcador not in prompt:
        raise ValueError(
            "O prompt não contém a seção '### INSTRUÇÃO'. "
            "Use montar_prompt() para criar o prompt base."
        )

    # Localiza o fim da linha de instrução para anexar o CoT logo abaixo
    idx = prompt.index(marcador) + len(marcador)
    # Encontra o próximo separador (fim do bloco de instrução)
    proximo_sep = prompt.find(SEPARADOR, idx)
    if proximo_sep == -1:
        # Instrução é o último bloco
        return prompt + "\n\n" + bloco_cot
    else:
        insercao = proximo_sep  # insere antes do próximo separador
        return prompt[:insercao] + f"\n\n{bloco_cot}" + prompt[insercao:]


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _validar_nao_vazio(valor: str, nome: str) -> None:
    """Garante que uma string não seja None nem vazia após strip()."""
    if not valor or not str(valor).strip():
        raise ValueError(
            f"O parâmetro '{nome}' não pode ser vazio ou None. "
            "Forneça um valor válido antes de montar o prompt."
        )


def _validar_exemplos(exemplos: list[dict]) -> None:
    """Valida a estrutura de cada exemplo de few-shot."""
    for i, ex in enumerate(exemplos):
        if not isinstance(ex, dict):
            raise ValueError(
                f"Exemplo {i} não é um dicionário. "
                "Cada exemplo deve ter o formato {'input': ..., 'output': ...}."
            )
        if "input" not in ex or "output" not in ex:
            raise ValueError(
                f"Exemplo {i} está faltando a chave 'input' ou 'output'. "
                f"Chaves encontradas: {list(ex.keys())}"
            )
        if not str(ex["input"]).strip() or not str(ex["output"]).strip():
            raise ValueError(
                f"Exemplo {i} tem 'input' ou 'output' vazio. "
                "Todos os exemplos devem ter valores preenchidos."
            )


# ---------------------------------------------------------------------------
# Demonstração (execução direta do módulo)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Teste: montar_prompt básico ===")
    p = montar_prompt(
        instrucao="Classifique o sentimento do texto a seguir.",
        input_dados="Carregador DC 150kW funcionou perfeitamente, bateria de 15% a 80% em 28 minutos!",
        contexto="Você está analisando avaliações de eletropostos e carregadores de carros elétricos em português.",
        formato_output="Responda APENAS com: POSITIVO, NEGATIVO, NEUTRO ou MISTO.",
    )
    print(p)

    print("\n=== Teste: adicionar_exemplos (few-shot) ===")
    exemplos = [
        {"input": "Carregador rápido, app intuitivo, excelente!", "output": "POSITIVO"},
        {"input": "Carregador fora de serviço pela 3ª vez, péssimo.", "output": "NEGATIVO"},
        {"input": "App bom mas carregador lento para o anunciado.", "output": "MISTO"},
    ]
    p_fs = adicionar_exemplos(p, exemplos)
    print(p_fs)

    print("\n=== Teste: adicionar_cot (chain-of-thought) ===")
    passos = [
        "Identifique expressões que indicam satisfação ou insatisfação com o eletroposto.",
        "Liste os aspectos positivos mencionados.",
        "Liste os aspectos negativos mencionados.",
        "Compare o peso de cada lado e classifique o sentimento predominante.",
    ]
    p_cot = adicionar_cot(p, passos)
    print(p_cot)
