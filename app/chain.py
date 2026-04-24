from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda


def criar_chain(retriever):
    modelo = ChatOpenAI(
        model="gpt-5.4-nano",
        temperature=0
    )

    prompt_llm = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Responda usando apenas o contexto recuperado e o histórico da conversa.\n\n"
            "Regras obrigatórias:\n"
            "- Se houver informação relevante no contexto, responda diretamente.\n"
            "- NÃO diga que 'não encontrou completamente' ou qualquer variação disso.\n"
            "- NÃO explique limitações do contexto.\n"
            "- NÃO misture respostas com avisos.\n\n"
            "Se NÃO houver informação suficiente:\n"
            "- responda apenas: 'Não encontrei essa informação nos documentos disponíveis.'\n\n"
            "Se houver informação parcial:\n"
            "- responda normalmente com o que encontrou, sem avisos."
        ),
        (
            "human",
            "Histórico da conversa:\n{historico}\n\n"
            "Pergunta atual:\n{query}\n\n"
            "Contexto recuperado:\n{contexto}\n\n"
            "Resposta:"
        )
    ]
)

    setup = {
        "query": RunnableLambda(lambda x: x["query"]),
        "historico": RunnableLambda(lambda x: x["historico"]),
        "contexto": RunnableLambda(lambda x: x["query"]) | retriever,
    }

    chain = setup | prompt_llm | modelo | StrOutputParser()

    return chain