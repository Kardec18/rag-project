from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

leitor_do_pdf = PdfReader("documents/Dipirona500mgMedley.pdf")

modelo = ChatOpenAI(
    model="gpt-5.4-nano",
    temperature=0
)

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

dados_do_pdf = FAISS.from_texts(
    textos, embeddings).as_retriever(search_kwargs={"k":3})

prompt_llm = ChatPromptTemplate.from_messages(
    [
        ("system", "Responda usando exclusivamente o conteúdo fornecido."),
        ("human","{query}\n\nContextos: \n{contexto}\n\nResposta:")
    ]
)

setup_and_retrieval = {
    "contexto": dados_do_pdf,
    "query": RunnablePassthrough()
}

chain_de_dados = setup_and_retrieval | prompt_llm | modelo | StrOutputParser()

pergunta = "Para que serve esse medicamento?"

resposta_llm = chain_de_dados.invoke(pergunta)

print(resposta_llm)
