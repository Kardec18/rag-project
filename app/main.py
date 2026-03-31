from embeddings import modelo_embedding
from vectorstore import carregar_indice
from retriever import obter_retriever
from chain import criar_chain
from dotenv import load_dotenv

load_dotenv()


def formatar_historico(historico):
    texto_historico = ""

    for interacao in historico:
        texto_historico += f"User: {interacao['pergunta']}\n"
        texto_historico += f"AI: {interacao['resposta']}\n\n"

    return texto_historico


def main():
    embeddings = modelo_embedding()
    vectorstore = carregar_indice("storage", embeddings)
    retriever = obter_retriever(vectorstore)
    chain = criar_chain(retriever)

    historico = []

    while True:
        pergunta = input("Digite sua pergunta (ou 'sair'): ").strip()

        if not pergunta:
            continue

        if pergunta.lower() == "sair":
            break

        historico_formatado = formatar_historico(historico)

        resposta = chain.invoke({
            "query": pergunta,
            "historico": historico_formatado
        })

        historico.append({
            "pergunta": pergunta,
            "resposta": resposta
        })

        print(resposta)


if __name__ == "__main__":
    main()