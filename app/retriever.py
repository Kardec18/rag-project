def obter_retriever(vectorstore, k=3):
    chunks_relevantes = vectorstore.as_retriever(search_kwargs={"k": k})

    return chunks_relevantes