from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

leitor_do_pdf = PdfReader("documents/Dipirona500mgMedley.pdf")

texto_completo = ""

paginas_do_pdf = leitor_do_pdf.pages

for pagina in paginas_do_pdf:
    texto_completo += pagina.extract_text()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

textos = text_splitter.split_text(texto_completo)

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002"
)

vetores = embeddings.embed_documents(textos)

vectorstore = FAISS.from_texts(textos, embeddings)

pergunta = "Para que serve esse medicamento?"

resposta = vectorstore.similarity_search(pergunta, k=3)

for info in resposta:
    print(f"Trecho encontrado: {info.page_content}\n")