from pypdf import PdfReader
import glob

def carregar_pdf():
    texto_total = ""

    for arquivo_pdf in glob.glob("documents/*.pdf"):
        total_de_arquivos = PdfReader(arquivo_pdf)

        pagina_do_arquivo = total_de_arquivos.pages

        for pagina in pagina_do_arquivo:
            texto = pagina.extract_text()

            if texto is not None:
                texto_total += texto

    return texto_total