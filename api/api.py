from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

from app.embeddings import modelo_embedding
from app.vectorstore import carregar_indice
from app.retriever import obter_retriever
from app.chain import criar_chain
from app.indexar import indexar

load_dotenv()

class UserQuestion(BaseModel):
    question: str
    history: str = ""

class AnswerResponse(BaseModel):
    answer: str

app = FastAPI()

questions = []

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {"status": "healthy"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_llm(user_input: UserQuestion):
    pergunta = user_input.question
    historico = user_input.history or ""

    if not pergunta.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    try:
        embeddings = modelo_embedding()
        vectorstore = carregar_indice("storage", embeddings)
        retriever = obter_retriever(vectorstore)
        chain = criar_chain(retriever)

        resposta = chain.invoke({
            "query": pergunta,
            "historico": historico
        })

        return {"answer": resposta}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a pergunta: {str(e)}"
        )
    
@app.post("/insert")
async def insert_pdf(file: UploadFile = File()):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo inválido.")
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")
    
    try:
        documents_path = Path("documents")
        documents_path.mkdir(exist_ok=True)

        file_path = documents_path / file.filename

        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        indexar()

        return {
            "message": "Arquivo inserido e indexado com sucesso",
            "filename": file.filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir arquivo: {str(e)}")
    
@app.post("/title")
async def gerar_titulo(user_input: UserQuestion):
    titulo = user_input.question[:50]  # simples (ou chama LLM)
    return {"title": titulo}