# Checkpoint 02 — Prompt Toolkit

**Domínio:** Eletropostos / Carregadores de Veículos Elétricos  
**Disciplina:** Cognitive and Semantic Computing (LCE)  
**Instituição:** FIAP

---

## Sobre o Projeto

Toolkit Python que aplica automaticamente quatro técnicas de prompting — **Zero-Shot**, **Few-Shot**, **Chain-of-Thought** e **Role Prompting** — a tarefas do domínio de eletropostos (classificação de solicitações, geração de respostas a clientes, análise de falhas em carregadores). O sistema compara os resultados entre técnicas, avalia métricas como consumo de tokens, latência e consistência, e recomenda automaticamente a abordagem mais eficaz para cada cenário.

---

## Estrutura do Projeto

```
checkpoint02-Prompt-Toolkit--lce-/
├── data/
│   └── inputs.json          # Inputs de teste por tarefa
├── docs/
│   └── CP02_NomeDoGrupo.pdf # Documentação técnica
├── output/                  # Gerado automaticamente pelo report.py
    ├── resultados.csv
    ├── recomendacao.json
    └── graficos/
        ├── grafico_tokens.png
        ├── grafico_tempo.png
        ├── grafico_heatmap.png
        └── grafico_consistencia.png
│   ├── resultados.csv
│   ├── grafico_tokens.png
│   ├── grafico_tempo.png
│   ├── grafico_heatmap.png
│   ├── grafico_consistencia.png
│   └── recomendacao.json
├── prompts/                 # Templates de prompts por técnica
├── src/
│   ├── evaluator.py         # Avaliação de tokens, acurácia, consistência
│   ├── llm_client.py        # Cliente da API (requests + dotenv)
|   ├── report.py            # Gera CSV, gráficos e recomendação automática
│   ├── tasks.py             # Definição das tarefas do domínio
│   └── techniques.py        # zero_shot, few_shot, cot, role_prompting
├── .gitignore
├── main.py                  # Executa todas as técnicas e coleta resultados
└── requirements.txt
```

---

## Pré-requisitos

- Python 3.10 ou superior
- Chave de API configurada em `.env` (veja abaixo)

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/CaioSilva2026/checkpoint02-Prompt-Toolkit--lce-.git
cd checkpoint02-Prompt-Toolkit--lce-
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a variável de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
OLLAMA_API_KEY=sua_chave_aqui
```

> O arquivo `.env` já está no `.gitignore` — nunca suba sua chave para o repositório.

---

## Execução

### Executar o toolkit principal (coleta de resultados)

```bash
python main.py
```

Isso itera sobre todas as tarefas e inputs definidos em `data/inputs.json`, aplica as quatro técnicas, imprime os resultados no terminal e ao final exibe o teste de temperatura.

### Gerar relatório, gráficos e recomendação

O relatório é gerado automaticamente ao final do main.py.

---

## Saídas Geradas (`output/`)

| Arquivo | Descrição |
|---|---|
| `resultados.csv` | Tabela completa com todas as execuções |
| `grafico_tokens.png` | Barras: consumo de tokens por técnica |
| `grafico_tempo.png` | Boxplot: latência por técnica |
| `grafico_heatmap.png` | Heatmap: tokens × tarefa × técnica |
| `grafico_consistencia.png` | Barras horizontais: consistência (%) |
| `recomendacao.json` | Técnica recomendada + score + justificativa |

---

## Técnicas Implementadas

| Técnica | Descrição |
|---|---|
| **Zero-Shot** | Instrução direta sem exemplos |
| **Few-Shot** | Instrução com exemplos de entrada/saída |
| **Chain-of-Thought** | Raciocínio passo a passo guiado |
| **Role Prompting** | Persona especialista via system prompt |

---

## Divisão de Tarefas

| Pessoa | Responsabilidade |
|---|---|
| Pessoa 1 | `src/llm_client.py` — integração com a API |
| Pessoa 2 | `src/tasks.py` + `data/inputs.json` — domínio e inputs |
| Pessoa 3 | `src/techniques.py` — implementação das 4 técnicas |
| Pessoa 4 | `src/evaluator.py` — métricas de avaliação |
| Pessoa 5 | `report.py` + `output/` + `README.md` + `docs/CP02_NomeDoGrupo.pdf` |

---

## Dependências

```
requests
python-dotenv
pandas
matplotlib
tiktoken
ollama
```
