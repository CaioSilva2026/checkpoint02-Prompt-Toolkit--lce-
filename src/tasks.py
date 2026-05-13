TASKS = [
    {
        "nome": "classificacao_ocorrencias",
        "tipo": "classificacao",
        "instrucao": "Classifique o relato em: FALHA_HARDWARE, FALHA_PAGAMENTO, FALHA_CONECTIVIDADE, USO_INCORRETO ou SEM_DEFEITO.",
        "formato_output": "Responda APENAS com a categoria, sem explicações adicionais.",
        "exemplos_fewshot": [
            {"input": "O conector travou e não saiu do carro.", "output": "FALHA_HARDWARE"},
            {"input": "Fui cobrado duas vezes na mesma sessão.", "output": "FALHA_PAGAMENTO"},
            {"input": "O app não conecta ao carregador via Wi-Fi.", "output": "FALHA_CONECTIVIDADE"},
        ],
        "passos_cot": [
            "Identifique qual componente está envolvido (cabo, app, pagamento, etc.)",
            "Avalie se o problema é causado pelo equipamento ou pelo usuário",
            "Verifique se há indicação de problema financeiro ou de rede",
            "Com base nos passos anteriores, escolha a categoria mais adequada",
        ],
        "persona": "analista_cx",
    },
    {
        "nome": "extracao_dados_tecnicos",
        "tipo": "extracao",
        "instrucao": "Extraia as informações estruturadas do relato sobre a sessão de carregamento.",
        "formato_output": "Retorne APENAS um JSON válido com as chaves: eletroposto, tipo_conector, potencia_kw, duracao_sessao, erro_reportado, numero_protocolo. Use null para dados ausentes.",
        "exemplos_fewshot": [
            {
                "input": "No eletroposto do Shopping Morumbi, o carregador CCS2 de 100kW travou após 15 minutos com erro E-04.",
                "output": '{"eletroposto": "Shopping Morumbi", "tipo_conector": "CCS2", "potencia_kw": "100kW", "duracao_sessao": "15 minutos", "erro_reportado": "E-04", "numero_protocolo": null}'
            },
        ],
        "passos_cot": [
            "Identifique o nome ou localização do eletroposto mencionado",
            "Procure pelo tipo de conector utilizado (CCS2, CHAdeMO, Type 2, GB/T)",
            "Identifique a potência em kW, se mencionada",
            "Procure por duração da sessão ou tempo de espera",
            "Identifique erros ou falhas específicas relatadas",
            "Procure por número de protocolo ou código de erro",
            "Monte o JSON com os dados encontrados, null para os ausentes",
        ],
        "persona": "especialista_infraestrutura",
    },
    {
        "nome": "resposta_suporte",
        "tipo": "geracao",
        "instrucao": "Gere uma resposta profissional e empática para a reclamação do usuário sobre o eletroposto.",
        "formato_output": "Escreva entre 3 e 5 frases. Reconheça o problema específico, apresente uma ação concreta e feche de forma positiva. Não use frases genéricas.",
        "exemplos_fewshot": [
            {
                "input": "Carregador quebrado pela terceira semana seguida no eletroposto do Ibirapuera.",
                "output": "Entendemos sua frustração — três semanas com o mesmo carregador fora de serviço não é aceitável. Escalamos a ocorrência para a equipe técnica regional com prioridade máxima. Nossa equipe entrará em contato em até 4 horas com previsão concreta de reparo."
            },
        ],
        "passos_cot": [
            "Identifique se o relato é positivo, negativo ou misto",
            "Reconheça o problema específico sem se esquivar",
            "Informe a ação tomada ou próximo passo concreto",
            "Se o problema foi crítico, demonstre urgência real",
            "Feche com compromisso ou chamada para ação",
            "Verifique que não há frases genéricas na resposta",
        ],
        "persona": "redator_comercial",
    },
]