# core/rag_chain.py

import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from core.logger import logger
from core.models import Filme

# --- CONSTANTES DE CONFIGURAÇÃO DO MÓDULO ---
# Construção do path movida para fora da função, como uma constante.
# Isso torna o código mais eficiente, legível e portável.
PROJECT_ROOT = Path(__file__).parent.parent
CATALOG_FILEPATH = PROJECT_ROOT / "data" / "movie_catalog.json"
# ---------------------------------------------

def load_catalog(filepath: Path = CATALOG_FILEPATH) -> List[Filme]:
    """
    Carrega o catálogo de filmes a partir do arquivo JSON, validando os dados
    e retornando uma lista de objetos Pydantic 'Filme'.
    O caminho para o arquivo é lido da constante do módulo.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        #* Pega a lista de dicionários da chave "filmes"
        movie_dicts = data.get("filmes", [])
        
        #* Converte cada dicionário em um objeto Pydantic Filme.
        #* Isso também valida se os dados no JSON estão corretos!
        catalog = [Filme(**movie_data) for movie_data in movie_dicts]
        
        logger.info(f"Catálogo com {len(catalog)} filmes carregado e validado com sucesso de '{filepath.name}'.")
        return catalog
    except FileNotFoundError:
        logger.error(f"Arquivo de catálogo não encontrado em {filepath}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Erro ao decodificar o JSON do arquivo {filepath}")
        return []

#! --- As outras funções do RAG virão aqui ---
# Em core/rag_chain.py, adicione esta função abaixo de load_catalog

def create_vector_store(movies: List[Filme]) -> InMemoryVectorStore:
    """
    Cria um VectorStore em memória a partir de uma lista de filmes.
    """
    if not movies:
        logger.warning("A lista de filmes está vazia. Nenhum VectorStore será criado.")
        return None

    # 1. Transforma cada objeto Filme em um Documento LangChain
    # A sinopse vai para o page_content para ser pesquisada.
    # O título vai para o metadata para ser recuperado junto.
    logger.info(f"Transformando {len(movies)} filmes em Documentos LangChain...")
    documents = [
        Document(
            page_content=movie.synopsis,
            metadata={"title": movie.title}
        ) for movie in movies
    ]

    # 2. Inicializa o modelo de embeddings da OpenAI
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 3. Cria o VectorStore e adiciona os documentos
    # Durante o .from_documents, o LangChain calcula os embeddings para cada documento
    # e os armazena em memória para busca rápida.
    logger.info("Criando o VectorStore e indexando os documentos...")
    vector_store = InMemoryVectorStore.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    logger.info("VectorStore criado com sucesso!")
    return vector_store

#! --- As outras funções do RAG virão aqui ---
# Em core/rag_chain.py, adicione esta função final

def create_rag_chain(vector_store: InMemoryVectorStore):
    """
    Cria e retorna uma chain RAG completa.
    """
    logger.info("Criando a chain RAG...")

    # 1. O Retriever: A interface para buscar documentos no VectorStore.
    # Ele pega uma string de pergunta e retorna uma lista de Documentos relevantes.
    retriever = vector_store.as_retriever()

    # 2. O Prompt Template: O "contrato" com o LLM.
    # Define como a pergunta do usuário e o contexto recuperado serão apresentados.
    RAG_PROMPT_TEMPLATE = """
    Você é um assistente de recomendação de filmes. Sua tarefa é gerar uma lista de 
    sugestões de filmes baseada EXCLUSIVAMENTE no contexto fornecido.
    Se o contexto não contiver filmes que correspondam à pergunta, informe que não 
    encontrou recomendações adequadas.
    Responda em português do Brasil, em um formato de lista simples.

    #* Contexto Relevante:
    {context}

    #* Pergunta do Usuário:
    {question}

    #* Sua Resposta:
    """
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

    # 3. O Modelo LLM: O cérebro que gera a resposta final.
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    #* Função auxiliar para formatar os documentos recuperados em uma única string
    def format_docs(docs: List[Document]) -> str:
        return "\n\n".join(f"Título: {doc.metadata['title']}\nSinopse: {doc.page_content}" for doc in docs)

    # 4. A Chain RAG com LCEL
    rag_chain = (
        RunnableParallel(
            context=(retriever | format_docs),
            question=RunnablePassthrough()
        )
        | prompt
        | model
    )

    logger.info("Chain RAG criada com sucesso!")
    return rag_chain