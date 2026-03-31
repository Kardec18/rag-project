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
                "Use apenas o contexto recuperado e o histórico da conversa para responder. "
                "Se a resposta não estiver no contexto, diga que não encontrou a informação. "
                "Não invente informações."
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