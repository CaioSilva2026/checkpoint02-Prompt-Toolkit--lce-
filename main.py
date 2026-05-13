from src.llm_client import gerar_resposta
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting

def main():

    tarefa = {
        "nome": "classificacao_ocorrencia",
        "instrucao": "Classifique o relato em: FALHA_HARDWARE, FALHA_PAGAMENTO, FALHA_CONECTIVIDADE, USO_INCORRETO ou SEM_DEFEITO.",
        "formato_output": "Responda APENAS com a categoria.",
    }

    input_dados = "Tentei carregar meu carro mas o cabo não encaixou no conector."

    exemplos = [
        {"input": "O cabo travou e não soltou.", "output": "FALHA_HARDWARE"},
        {"input": "Cobrou duas vezes no cartão.", "output": "FALHA_PAGAMENTO"},
    ]

    passos = [
        "Identifique o componente envolvido",
        "Avalie se é falha do equipamento ou do usuário",
        "Escolha a categoria mais adequada",
    ]

    # 1. Zero-Shot
    prompt_zs = zero_shot(tarefa, input_dados)
    resultado_zs = gerar_resposta(prompt=prompt_zs)
    print("Zero-Shot:", resultado_zs["resposta"])

    # 2. Few-Shot
    prompt_fs = few_shot(tarefa, input_dados, exemplos)
    resultado_fs = gerar_resposta(prompt=prompt_fs)
    print("Few-Shot:", resultado_fs["resposta"])

    # 3. Chain-of-Thought
    prompt_cot = chain_of_thought(tarefa, input_dados, passos)
    resultado_cot = gerar_resposta(prompt=prompt_cot)
    print("CoT:", resultado_cot["resposta"])

    # 4. Role Prompting — única técnica que passa system separado
    system, user = role_prompting(tarefa, input_dados, "analista_cx")
    resultado_role = gerar_resposta(prompt=user, system=system)
    print("Role:", resultado_role["resposta"])

if __name__ == "__main__":
    main()