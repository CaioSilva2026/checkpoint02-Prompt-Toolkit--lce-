import json
import os

# from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot

def montar_prompt(instrucao, contexto, input_dados, formato_output):
    """
    PLACEHOLDER — substitua por: from src.prompt_builder import montar_prompt
    """
    return (
        f"Instrução: {instrucao}\n"
        f"Contexto: {contexto}\n"
        f"Input: {input_dados}\n"
        f"Formato esperado: {formato_output}"
    )

def adicionar_exemplos(prompt: str, exemplos: list) -> str:
    """
    PLACEHOLDER — substitua por: from src.prompt_builder import adicionar_exemplos
    """
    bloco = "\n\nExemplos:\n"
    for ex in exemplos:
        bloco += f'Input: "{ex["input"]}" → Output: "{ex["output"]}"\n'
    return bloco + "\n" + prompt

def adicionar_cot(prompt: str, passos: list) -> str:
    """
    PLACEHOLDER — substitua por: from src.prompt_builder import adicionar_cot
    """
    bloco = "Analise passo a passo:\n"
    for i, passo in enumerate(passos, start=1):
        bloco += f"  Passo {i}: {passo}\n"
    bloco += "\nApenas após seguir todos os passos, forneça a resposta final.\n\n"
    return bloco + prompt

def carregar_personas(caminho: str = "prompts/system_prompts.json") -> dict:
    if not os.path.exists(caminho):
        raise FileNotFoundError(
            f"[role_prompting] Arquivo de personas não encontrado: {caminho}"
        )
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


#Técnica 1: Zero-Shot
def zero_shot(tarefa: dict, input_dados: str) -> str:
    instrucao      = tarefa["instrucao"]
    formato_output = tarefa["formato_output"]
    contexto       = "Nenhum exemplo fornecido. Responda com base no seu conhecimento."

    prompt = montar_prompt(
        instrucao=instrucao,
        contexto=contexto,
        input_dados=input_dados,
        formato_output=formato_output
    )

    return prompt


#Técnica 2: Few-Shot
def few_shot(tarefa: dict, input_dados: str, exemplos: list) -> str:
    if not exemplos or len(exemplos) == 0:
        raise ValueError("[few_shot] A lista de exemplos não pode estar vazia.")

    instrucao      = tarefa["instrucao"]
    formato_output = tarefa["formato_output"]
    contexto       = "Use os exemplos abaixo para entender o padrão esperado de resposta."

    prompt_base = montar_prompt(
        instrucao=instrucao,
        contexto=contexto,
        input_dados=input_dados,
        formato_output=formato_output
    )

    prompt_final = adicionar_exemplos(
        prompt=prompt_base,
        exemplos=exemplos
    )

    return prompt_final


#Técnica 3: Chain-of-Thought
def chain_of_thought(tarefa: dict, input_dados: str, passos: list) -> str:
    if not passos or len(passos) == 0:
        raise ValueError("[chain_of_thought] A lista de passos não pode estar vazia.")

    instrucao      = tarefa["instrucao"]
    formato_output = tarefa["formato_output"]
    contexto       = "Antes de responder, siga os passos de raciocínio indicados."

    prompt_base = montar_prompt(
        instrucao=instrucao,
        contexto=contexto,
        input_dados=input_dados,
        formato_output=formato_output
    )

    prompt_final = adicionar_cot(
        prompt=prompt_base,
        passos=passos
    )

    return prompt_final

#Técnica 4: Role Prompting
def role_prompting(tarefa: dict, input_dados: str, persona: str) -> tuple:
    instrucao      = tarefa["instrucao"]
    formato_output = tarefa["formato_output"]
    contexto       = "Responda conforme seu papel e especialidade."

    personas = carregar_personas()

    if persona not in personas:
        raise ValueError(
            f"[role_prompting] Persona '{persona}' não encontrada. "
            f"Personas disponíveis: {list(personas.keys())}"
        )

    system_prompt = personas[persona]["system_prompt"]

    user_prompt = montar_prompt(
        instrucao=instrucao,
        contexto=contexto,
        input_dados=input_dados,
        formato_output=formato_output
    )

    return (system_prompt, user_prompt)