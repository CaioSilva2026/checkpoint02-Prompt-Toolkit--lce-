import json
from src.llm_client import gerar_resposta
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TASKS
from src.evaluator import avaliar_tokens, avaliar_consistencia, testar_temperatura

from src.report import gerar_relatorio

def carregar_inputs(caminho: str = "data/inputs.json") -> dict:
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def executar_tecnicas(tarefa: dict, input_dados: str) -> dict:

    resultados = {}

    # 1. Zero-Shot
    prompt_zs = zero_shot(tarefa, input_dados)
    resultados["zero_shot"] = gerar_resposta(prompt=prompt_zs)

    # 2. Few-Shot
    prompt_fs = few_shot(tarefa, input_dados, tarefa["exemplos_fewshot"])
    resultados["few_shot"] = gerar_resposta(prompt=prompt_fs)

    # 3. Chain-of-Thought
    prompt_cot = chain_of_thought(tarefa, input_dados, tarefa["passos_cot"])
    resultados["chain_of_thought"] = gerar_resposta(prompt=prompt_cot)

    # 4. Role Prompting
    system, user = role_prompting(tarefa, input_dados, tarefa["persona"])
    resultados["role_prompting"] = gerar_resposta(prompt=user, system=system)

    return resultados


def medir_consistencia_real(tarefa: dict, input_dados: str, n: int = 3) -> dict:

    print(f"\n  [CONSISTÊNCIA] Rodando input representativo {n}x por técnica...")
    consistencias = {}

    # Zero-Shot
    respostas = []
    prompt_zs = zero_shot(tarefa, input_dados)
    for i in range(n):
        r = gerar_resposta(prompt=prompt_zs)
        respostas.append(r["resposta"])
        print(f"    Zero-Shot  [{i + 1}/{n}]: {r['resposta']}")
    consistencias["zero_shot"] = avaliar_consistencia(respostas)

    # Few-Shot
    respostas = []
    prompt_fs = few_shot(tarefa, input_dados, tarefa["exemplos_fewshot"])
    for i in range(n):
        r = gerar_resposta(prompt=prompt_fs)
        respostas.append(r["resposta"])
        print(f"    Few-Shot   [{i + 1}/{n}]: {r['resposta']}")
    consistencias["few_shot"] = avaliar_consistencia(respostas)

    # Chain-of-Thought
    respostas = []
    prompt_cot = chain_of_thought(tarefa, input_dados, tarefa["passos_cot"])
    for i in range(n):
        r = gerar_resposta(prompt=prompt_cot)
        respostas.append(r["resposta"])
        print(f"    CoT        [{i + 1}/{n}]: {r['resposta']}")
    consistencias["chain_of_thought"] = avaliar_consistencia(respostas)

    # Role Prompting
    respostas = []
    system, user = role_prompting(tarefa, input_dados, tarefa["persona"])
    for i in range(n):
        r = gerar_resposta(prompt=user, system=system)
        respostas.append(r["resposta"])
        print(f"    Role       [{i + 1}/{n}]: {r['resposta']}")
    consistencias["role_prompting"] = avaliar_consistencia(respostas)

    return consistencias

def imprimir_resultado(tarefa_nome: str, input_dados: str, resultados: dict) -> None:

    separador = "-" * 60
    print(f"\n{separador}")
    print(f"TAREFA : {tarefa_nome}")
    print(f"INPUT  : {input_dados}")
    print(separador)
    for tecnica, resultado in resultados.items():
        print(f"  {tecnica:<20}: {resultado['resposta']}")
        print(f"  {'tokens_prompt':<20}: {resultado['tokens_prompt']}")
        print(f"  {'tokens_resposta':<20}: {resultado['tokens_resposta']}")
        print(f"  {'tempo_ms':<20}: {resultado['tempo_ms']}ms")
        print()

def main():
    print("=" * 60)
    print("PROMPT TOOLKIT — Checkpoint 02")
    print("Domínio: Eletropostos / Carregadores de Veículos Elétricos")
    print("=" * 60)

    # Carrega todos os inputs do domínio
    todos_inputs = carregar_inputs()

    # Acumula todos os resultados para o relatório
    todos_resultados = []

    consistencias_por_tarefas = {}

    # Itera sobre cada tarefa definida em tasks.py
    for tarefa in TASKS:
        nome_tarefa = tarefa["nome"]
        inputs_da_tarefa = todos_inputs.get(nome_tarefa, [])

        if not inputs_da_tarefa:
            print(f"\n[AVISO] Nenhum input encontrado para a tarefa '{nome_tarefa}'. Pulando.")
            continue

        print(f"\n{'=' * 60}")
        print(f"INICIANDO TAREFA: {nome_tarefa.upper()}")
        print(f"{'=' * 60}")

        respostas_por_input = []

        # Itera sobre cada input da tarefa
        for input_dados in inputs_da_tarefa:
            resultados = executar_tecnicas(tarefa, input_dados)
            imprimir_resultado(nome_tarefa, input_dados, resultados)

            # Avalia tokens de cada técnica
            for tecnica, resultado in resultados.items():
                tokens = avaliar_tokens(resultado["resposta"])
                resultado["tokens_contados"] = tokens

            respostas_por_input.append({
                "input": input_dados,
                "resultados": resultados
            })

        # Mede consistência por técnica (mesma tarefa, todos os inputs)
        input_representativo = inputs_da_tarefa[0]
        consistencias = medir_consistencia_real(tarefa=tarefa,input_dados=input_representativo,n=3)
        consistencias_por_tarefas[nome_tarefa] = consistencias

        print(f"\n  Consistência real (input representativo — 3 repetições):")
        for tecnica, valor in consistencias.items():
            print(f"    {tecnica:<25}: {valor * 100:.0f}%")
        todos_resultados.append({
        "tarefa": nome_tarefa,
        "inputs": respostas_por_input
        })

    print(f"\n{'=' * 60}")
    print("TESTE DE TEMPERATURA")
    print(f"{'=' * 60}")

    tarefa_teste = TASKS[0]
    input_teste = todos_inputs.get(tarefa_teste["nome"], [])[0]
    prompt_teste = zero_shot(tarefa_teste, input_teste)

    resultados_temp = testar_temperatura(
        prompt=prompt_teste,
        gerar_resposta_fn=gerar_resposta,
        temps=[0.1, 0.5, 1.0]
    )

    for r in resultados_temp:
        print(f"  Temperatura {r['temperatura']} → {r['resposta']}")

    consistencias_globais = {}
    for tecnica in ["zero_shot", "few_shot", "chain_of_thought", "role_prompting"]:
        valores = [
            consistencias_por_tarefas[t][tecnica]
            for t in consistencias_por_tarefas
            if tecnica in consistencias_por_tarefas[t]
        ]
        consistencias_globais[tecnica] = sum(valores) / len(valores) if valores else 0.0

    print(f"\n{'=' * 60}")
    print("CONSISTÊNCIA GLOBAL (média entre tarefas):")
    for tecnica, valor in consistencias_globais.items():
        print(f"  {tecnica:<25}: {valor * 100:.0f}%")

    gerar_relatorio(
        todos_resultados=todos_resultados,
        consistencias=consistencias_globais
    )

if __name__ == "__main__":
    main()