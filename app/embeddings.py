from langchain_openai import OpenAIEmbeddings

def modelo_embedding():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002"
    )

    return embeddings