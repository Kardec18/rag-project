from langchain_text_splitters import RecursiveCharacterTextSplitter

def dividir_texto(texto):
    separador_de_texto = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
    separators=["\n\n", "\n", " ", ""]
    )

    texto_separado = separador_de_texto.split_text(texto)

    return texto_separado