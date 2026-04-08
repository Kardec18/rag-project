from app.loader import carregar_pdf
from app.splitter import dividir_texto
from app.embeddings import modelo_embedding
from app.vectorstore import criar_indice, salvar_indice
from dotenv import load_dotenv

load_dotenv()

def indexar():
    texto = carregar_pdf()

    chunks = dividir_texto(texto)

    embeddings = modelo_embedding()

    indice = criar_indice(chunks, embeddings)

    salvar_indice(indice, "storage")

if __name__ == "__main__":
    indexar()