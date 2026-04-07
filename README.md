# Projeto RAG com PDFs (Langchain + LLM)

Este projeto implementa um sistema de Retrieval-Augmented Generation (RAG) para consulta inteligente de documentos PDF, retornando respostas baseadas exclusivamente no conteúdo carregado.

O pipeline inclui ingestão de documentos, geração de embeddings, indexação vetorial com FAISS e recuperação de contexto para geração de respostas com LLM.

## Objetivo do projeto

Este projeto foi desenvolvido com foco em aprendizado de conceitos fundamentais de RAG e como base para evolução para um sistema produtivo com práticas de MLOps.

## Funcionalidades

- Leitura de múltiplos PDFs

- Divisão de texto em chunks

- Geração de embeddings

- Armazenamento vetorial em FAISS

- Recuperação de contexto relevante

- Interface CLI interativa com histórico

## Arquitetura
```
app/
├── loader.py        # Carrega PDFs
├── splitter.py      # Divide texto em chunks
├── embeddings.py    # Gera embeddings
├── vectorstore.py   # Cria e salva índice FAISS
├── retriever.py     # Recupera contexto
├── chain.py         # Integra LLM + contexto
├── indexar.py       # Pipeline de indexação
└── main.py          # CLI principal
```

## Como Executar

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

### 5. Execute o script
```bash
python app/indexar.py # Execute primeiro o indexar.py, para criar o diretório storage

python app/main.py # Execute em seguida o main.py para iniciar a interface CLI
```

## Estrutura de dados
```bash
documents/
├── *.pdf
storage/
├── index.faiss
├── index.pkl
```

## Exemplo de uso
```
Pergunta:
> Digite sua pergunta (ou 'sair'): Qual medicamento é indicado para dor de cabeça?

Resposta:
> O contexto recuperado indica que **paracetamol** é indicado para **alívio temporário de dores leves a moderadas**, incluindo **dor de cabeça**.
```

## Limitações

- Responde apenas com base nos documentos carregados
- Pode falhar se o contexto não for encontrado
- Não possui interface web (apenas CLI)

## Próximas melhorias

- [ ] Criar API com FastAPI
- [ ] Adicionar interface com Streamlit
- [ ] Deploy em cloud
- [ ] Monitoramento de queries
- [ ] Versionamento de embeddings

## Tecnologias

- Python
- LangChain
- OpenAI API
- FAISS (Vector Store)
- dotenv (gerenciamento de variáveis de ambiente)

## Pipeline do sistema

1. Carregamento dos PDFs
2. Divisão em chunks
3. Geração de embeddings
4. Indexação vetorial (FAISS)
5. Recuperação de contexto relevante
6. Geração de resposta com LLM