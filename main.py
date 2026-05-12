from llm_client import gerar_resposta


def main():

    prompt = "Explique rapidamente o que é uma IA."

    resposta = gerar_resposta(prompt)

    print("\nRESPOSTA:\n")
    print(resposta)


if __name__ == "__main__":
    main()