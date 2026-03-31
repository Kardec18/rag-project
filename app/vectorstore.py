from langchain_community.vectorstores import FAISS

def criar_indice(chunks, embeddings):
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)

    return vectorstore

def salvar_indice(vectorstore, caminho):
    vectorstore.save_local(caminho)

def carregar_indice(caminho, embeddings):
    vectorstore = FAISS.load_local(
        caminho, 
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore