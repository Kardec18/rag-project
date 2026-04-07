from langchain_text_splitters import RecursiveCharacterTextSplitter

def dividir_texto(texto):
    separador_de_texto = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
    )

    texto_separado = separador_de_texto.split_text(texto)

    return texto_separado