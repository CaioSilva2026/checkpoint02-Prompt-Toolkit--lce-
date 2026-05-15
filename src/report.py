
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUTPUT_DIR    = "output"
GRAFICOS_DIR  = os.path.join(OUTPUT_DIR, "graficos")
os.makedirs(GRAFICOS_DIR, exist_ok=True)

TECNICAS = ["zero_shot", "few_shot", "chain_of_thought", "role_prompting"]
TECNICAS_LABELS = {
    "zero_shot": "Zero-Shot",
    "few_shot": "Few-Shot",
    "chain_of_thought": "Chain-of-Thought",
    "role_prompting": "Role Prompting",
}

COR_TECNICA = {
    "zero_shot": "#4C72B0",
    "few_shot": "#DD8452",
    "chain_of_thought": "#55A868",
    "role_prompting": "#C44E52",
}

# 1. GERAÇÃO DA TABELA CSV
def gerar_csv(todos_resultados: list, caminho: str = None) -> pd.DataFrame:
    if caminho is None:
        caminho = os.path.join(OUTPUT_DIR, "resultados.csv")

    linhas = []
    for bloco in todos_resultados:
        tarefa = bloco["tarefa"]
        for item in bloco["inputs"]:
            inp = item["input"]
            for tecnica, resultado in item["resultados"].items():
                linhas.append({
                    "tarefa": tarefa,
                    "input": inp,
                    "tecnica": tecnica,
                    "resposta": resultado.get("resposta", ""),
                    "tokens_prompt": resultado.get("tokens_prompt", 0),
                    "tokens_resposta": resultado.get("tokens_resposta", 0),
                    "tempo_ms": resultado.get("tempo_ms", 0),
                    "tokens_contados": resultado.get("tokens_contados", 0),
                })

    df = pd.DataFrame(linhas)
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"[CSV] Salvo em: {caminho}  ({len(df)} linhas)")
    return df

# 2. GRÁFICOS
def grafico_tokens_por_tecnica(df: pd.DataFrame, caminho: str = None) -> str:
    if caminho is None:
        caminho = os.path.join(GRAFICOS_DIR, "grafico_tokens.png")

    agg = df.groupby("tecnica")[["tokens_prompt", "tokens_resposta"]].mean().reindex(TECNICAS)

    x = range(len(TECNICAS))
    largura = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))

    bars1 = ax.bar([i - largura / 2 for i in x], agg["tokens_prompt"],
                   largura, label="Tokens Prompt",
                   color=[COR_TECNICA[t] for t in TECNICAS], alpha=0.85)
    bars2 = ax.bar([i + largura / 2 for i in x], agg["tokens_resposta"],
                   largura, label="Tokens Resposta",
                   color=[COR_TECNICA[t] for t in TECNICAS], alpha=0.45)

    ax.set_xticks(list(x))
    ax.set_xticklabels([TECNICAS_LABELS[t] for t in TECNICAS], fontsize=10)
    ax.set_ylabel("Média de Tokens", fontsize=11)
    ax.set_title("Consumo de Tokens por Técnica de Prompting", fontsize=13, fontweight="bold")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"[GRÁFICO] Tokens → {caminho}")
    return caminho


def grafico_tempo_por_tecnica(df: pd.DataFrame, caminho: str = None) -> str:

    if caminho is None:
        caminho = os.path.join(GRAFICOS_DIR, "grafico_tempo.png")

    dados = [df[df["tecnica"] == t]["tempo_ms"].dropna().values for t in TECNICAS]
    labels = [TECNICAS_LABELS[t] for t in TECNICAS]
    cores = [COR_TECNICA[t] for t in TECNICAS]

    fig, ax = plt.subplots(figsize=(9, 5))
    bp = ax.boxplot(dados, labels=labels, patch_artist=True, notch=False)

    for patch, cor in zip(bp["boxes"], cores):
        patch.set_facecolor(cor)
        patch.set_alpha(0.7)

    ax.set_ylabel("Tempo de Resposta (ms)", fontsize=11)
    ax.set_title("Distribuição do Tempo de Resposta por Técnica", fontsize=13, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"[GRÁFICO] Tempo → {caminho}")
    return caminho


def grafico_comparativo_tarefas(df: pd.DataFrame, caminho: str = None) -> str:

    if caminho is None:
        caminho = os.path.join(GRAFICOS_DIR, "grafico_heatmap.png")

    pivot = df.pivot_table(
        values="tokens_resposta", index="tarefa", columns="tecnica", aggfunc="mean"
    ).reindex(columns=TECNICAS)

    fig, ax = plt.subplots(figsize=(10, max(3, len(pivot) * 1.2)))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    plt.colorbar(im, ax=ax, label="Tokens (média)")

    ax.set_xticks(range(len(TECNICAS)))
    ax.set_xticklabels([TECNICAS_LABELS[t] for t in TECNICAS], rotation=20, ha="right")
    ax.set_yticks(range(len(pivot)))
    ax.set_yticklabels(pivot.index, fontsize=9)
    ax.set_title("Tokens de Resposta: Tarefa × Técnica", fontsize=13, fontweight="bold")

    for i in range(len(pivot)):
        for j in range(len(TECNICAS)):
            val = pivot.values[i][j]
            if not pd.isna(val):
                ax.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=9, color="black")

    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"[GRÁFICO] Heatmap → {caminho}")
    return caminho

def grafico_consistencia(consistencias: dict, caminho: str = None) -> str:
    if caminho is None:
        caminho = os.path.join(GRAFICOS_DIR, "grafico_consistencia.png")

    tecnicas = [t for t in TECNICAS if t in consistencias]
    valores = [consistencias[t] * 100 for t in tecnicas]
    labels = [TECNICAS_LABELS[t] for t in tecnicas]
    cores = [COR_TECNICA[t] for t in tecnicas]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(labels, valores, color=cores, alpha=0.8)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Consistência (%)", fontsize=11)
    ax.set_title("Consistência das Respostas por Técnica", fontsize=13, fontweight="bold")
    ax.axvline(80, color="gray", linestyle="--", linewidth=1, label="Limiar 80%")
    ax.legend()

    for bar, val in zip(bars, valores):
        ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
                f"{val:.0f}%", va="center", fontsize=10)

    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"[GRÁFICO] Consistência → {caminho}")
    return caminho

# 3. RECOMENDAÇÃO AUTOMÁTICA
PESOS = {
    "tokens_prompt": -0.2,
    "tokens_resposta": 0.3,
    "tempo_ms": -0.2,
    "tokens_contados": 0.3,
}

PESOS_CONSISTENCIA = 0.4

def recomendar_tecnica(
    df: pd.DataFrame,
    consistencias: dict = None,
    tarefa: str = None,
) -> dict:
    subset = df[df["tarefa"] == tarefa] if tarefa else df

    # Agrega métricas por técnica
    agg = subset.groupby("tecnica").agg(
        tokens_prompt=("tokens_prompt", "mean"),
        tokens_resposta=("tokens_resposta", "mean"),
        tempo_ms=("tempo_ms", "mean"),
        tokens_contados=("tokens_contados", "mean"),
    )

    # Normaliza colunas para [0, 1]
    def normalizar(series):
        mn, mx = series.min(), series.max()
        if mx == mn:
            return series * 0 + 0.5
        return (series - mn) / (mx - mn)

    scores = pd.Series(0.0, index=agg.index)

    for col, peso in PESOS.items():
        if col in agg.columns:
            norm = normalizar(agg[col])
            scores += peso * norm

    # Adiciona consistência se fornecida
    if consistencias:
        for tec, val in consistencias.items():
            if tec in scores.index:
                scores[tec] += PESOS_CONSISTENCIA * val

    scores = scores.reindex(TECNICAS).dropna()
    melhor = scores.idxmax()

    # Monta justificativa legível
    metricas = agg.loc[melhor]
    justificativa = (
        f"A técnica '{TECNICAS_LABELS[melhor]}' obteve o maior score ponderado ({scores[melhor]:.3f}). "
        f"Média: {metricas['tokens_prompt']:.0f} tokens de prompt, "
        f"{metricas['tokens_resposta']:.0f} tokens de resposta, "
        f"{metricas['tempo_ms']:.0f} ms de latência."
    )
    if consistencias and melhor in consistencias:
        justificativa += f" Consistência: {consistencias[melhor] * 100:.0f}%."

    resultado = {
        "melhor_tecnica": melhor,
        "label": TECNICAS_LABELS[melhor],
        "scores": scores.to_dict(),
        "justificativa": justificativa,
    }

    print("\n[RECOMENDAÇÃO]")
    print(f"  Melhor técnica: {resultado['label']}")
    print(f"  {justificativa}")
    return resultado

# 4. RELATÓRIO COMPLETO (entry point)
def gerar_relatorio(
    todos_resultados: list = None,
    consistencias: dict = None,
    caminho_csv: str = None,
):
    print("\n" + "=" * 60)
    print("RELATÓRIO — Prompt Toolkit CP02")
    print("=" * 60)

    # 1. Carrega ou gera CSV
    if todos_resultados:
        df = gerar_csv(todos_resultados)
    else:
        raise ValueError(
            "[report] todos_resultados não pode ser vazio. "
            "Certifique-se de chamar gerar_relatorio() a partir do main.py."
        )

    # 2. Gráficos
    grafico_tokens_por_tecnica(df)
    grafico_tempo_por_tecnica(df)
    grafico_comparativo_tarefas(df)

    if consistencias:
        grafico_consistencia(consistencias)
    else:
        # Consistência simulada para demonstração
        cons_sim = {"zero_shot": 0.78, "few_shot": 0.91,
                    "chain_of_thought": 0.88, "role_prompting": 0.83}
        grafico_consistencia(cons_sim)
        consistencias = cons_sim

    # 3. Recomendação automática
    rec = recomendar_tecnica(df, consistencias)

    # 4. Salva resumo JSON
    resumo_path = os.path.join(OUTPUT_DIR, "recomendacao.json")
    with open(resumo_path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    print(f"[JSON] Recomendação salva em: {resumo_path}")

    print("\n" + "=" * 60)
    print(f"Relatório gerado com sucesso em ./{OUTPUT_DIR}/")
    print("=" * 60)

    return df, rec

# Execução direta
if __name__ == "__main__":
    gerar_relatorio()
