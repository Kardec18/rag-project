# 🧠 Projeto RAG com PDFs (LangChain + API + Docker)

Este projeto implementa um sistema de Retrieval-Augmented Generation (RAG) para consulta inteligente de documentos PDF, retornando respostas baseadas exclusivamente no conteúdo carregado.

O sistema evoluiu de uma aplicação CLI para uma API com FastAPI, containerizada com Docker, permitindo execução padronizada e pronta para ambientes mais próximos de produção.

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

- Aprender conceitos fundamentais de RAG
- Construir uma aplicação real com API
- Aplicar conceitos de containerização com Docker
- Servir como base para evolução em MLOps / AI Platform

## ⚙️ Funcionalidades

- Leitura de múltiplos PDFs
- Divisão de texto em chunks
- Geração de embeddings
- Armazenamento vetorial com FAISS
- Recuperação de contexto relevante
- Geração de respostas com LLM
- API REST com FastAPI
- Upload de novos documentos via API
- Indexação automática de documentos
- Containerização com Docker

## 🏗️ Arquitetura
```
.
├── api/
│   └── api.py              # API FastAPI
├── app/
│   ├── loader.py           # Carrega PDFs
│   ├── splitter.py         # Divide texto em chunks
│   ├── embeddings.py       # Gera embeddings
│   ├── vectorstore.py      # Cria e salva índice FAISS
│   ├── retriever.py        # Recupera contexto
│   ├── chain.py            # Integra LLM + contexto
│   ├── indexar.py          # Pipeline de indexação
│   └── main.py             # CLI (legado)
├── documents/              # PDFs utilizados
├── storage/                # Índice vetorial FAISS
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
└── README.md
```

## 🚀 Como Executar

### Opção 1 - Execução com Docker (recomendado)

### 1. Criar o arquivo .env
```env
OPENAI_API_KEY=sua_chave 
```

### 2. Subir a aplicação
```
docker compose up --build
```

A API ficará disponível em:

```
http://localhost:8000
```

### Opção 2 - Execução local (sem Docker)

### 1. Clone o projeto
```bash
git clone <repo>

cd rag-project
```

### 2. Crie o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Para iniciar o ambiente virtual em ambientes Linux/macOS
venv\Scripts\activate     # Para iniciar o ambiente virtual em ambientes Windows
```

### 3. Instale as libs
```bash
pip install -r requirements.txt
```

### 4. Crie um arquivo `.env` na raiz do projeto (Crie uma API KEY no painel da OPENAI):
```env
OPENAI_API_KEY=sua_chave 
```

### 5. Executar indexação
```bash
python -m app.indexar # Execute primeiro o indexar.py, para criar o diretório storage
```

### 6. Subir a API
```bash
uvicorn api.api:app --reload
```

## 🧪 Testando a API via cURL

### Health Check
```
curl -X GET http://127.0.0.1:8000/health
```

### Fazer pergunta
```
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Cimegripe serve para o que?"}'
```

### Upload de PDF
```
curl -X POST http://127.0.0.1:8000/insert \
  -F "file=@/caminho/para/seu/arquivo.pdf"
```

## 📦 Estrutura de dados
```bash
documents/
├── *.pdf
storage/
├── index.faiss
├── index.pkl
```

## 🧠 Pipeline do sistema
1. Carregamento dos PDFs
2. Divisão em chunks
3. Geração de embeddings
4. Indexação vetorial (FAISS)
5. Recuperação de contexto relevante
6. Geração de resposta com LLM

## ⚠️ Limitações

- Responde apenas com base nos documentos carregados
- Não possui autenticação na API
- Indexação pode aumentar o tempo de startup
- Não possui persistência externa (dados ficam no container)

## Próximas melhorias

- [ ] Observabilidade
- [ ] Deploy em Kubernetes

## Tecnologias

- Python
- FastAPI
- LangChain
- OpenAI API
- FAISS
- Docker

## 💡 Considerações

Este projeto representa a evolução de um RAG simples para uma aplicação mais próxima de um ambiente real, incorporando:

- API REST
- Containerização
- Organização modular

Servindo como base para estudos em:

- MLOps
- AI Platform Engineering
- Sistemas com LLM em produção