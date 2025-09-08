# main.py
import sys
from pathlib import Path

# Adiciona a raiz do projeto (a pasta 'movie_project_rag') ao path do Python
# Isso garante que o Python sempre encontre o módulo 'core'
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
from core.logger import logger
from core.rag_chain import load_catalog, create_vector_store, create_rag_chain

def main():
    """
    Função principal que orquestra a aplicação RAG de recomendação de filmes.
    """
    # 1. Fase de Setup
    # Carrega as variáveis de ambiente (API Key)
    load_dotenv()
    logger.info("Iniciando a aplicação de recomendação de filmes RAG...")

    # Carrega o catálogo de filmes do nosso arquivo JSON
    movies = load_catalog()
    if not movies:
        logger.error("Nenhum filme foi carregado. Encerrando a aplicação.")
        return

    # Cria o VectorStore a partir dos filmes carregados
    vector_store = create_vector_store(movies)
    if not vector_store:
        logger.error("Falha ao criar o VectorStore. Encerrando a aplicação.")
        return

    # Cria a chain RAG principal
    chain = create_rag_chain(vector_store)

    logger.info("\n--- Assistente de Recomendação de Filmes Pronto ---")

    # 2. Fase Interativa (Loop)
    while True:
        # Pede a entrada do usuário
        question = input("\n> Descreva o tipo de filme que você gostaria de ver (ou digite 'sair' para terminar): ")

        # Condição de saída do loop
        if question.lower() == 'sair':
            break

        # Invoca a chain com a pergunta do usuário
        logger.info("Buscando recomendações...")
        response = chain.invoke(question)

        # Imprime a resposta formatada do LLM
        # A resposta da chain é um objeto AIMessage, então acessamos seu conteúdo com .content
        print(f"\nIA: {response.content}")

    logger.info("--- Aplicação encerrada. Até a próxima! ---")


if __name__ == "__main__":
    main()
