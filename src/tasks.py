TASKS = [
    {
        "id": "classificacao_ocorrencias",
        "nome": "Classificação de Ocorrências",
        "descricao": "Recebe um relato de problema com o carregador e classifica o tipo de falha.",
        "categorias": ["FALHA_HARDWARE", "FALHA_PAGAMENTO", "FALHA_CONECTIVIDADE", "USO_INCORRETO", "SEM_DEFEITO"],
        "output_esperado": "uma categoria apenas"
    },
    {
        "id": "extracao_dados_tecnicos",
        "nome": "Extração de Dados Técnicos",
        "descricao": "Recebe descrição de um eletroposto e extrai campos estruturados em JSON.",
        "campos": ["potencia_kw", "tipo_conector", "tensao", "localizacao", "compatibilidade"],
        "output_esperado": "JSON com os campos"
    },
    {
        "id": "resposta_suporte",
        "nome": "Geração de Resposta de Suporte",
        "descricao": "Recebe relato de cliente insatisfeito e gera resposta formal de suporte técnico.",
        "output_esperado": "texto formal de resposta"
    }
]