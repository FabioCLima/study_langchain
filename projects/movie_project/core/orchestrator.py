# core/orchestrator.py
'''
Pense em um "grafo" como um fluxograma de processamento de dados, onde cada caixa é uma tarefa e as setas indicam como os dados fluem.
'''


from typing import List, Dict
from langchain_core.runnables import RunnablePassthrough
from core.models import MovieList

from core.chain_suggestion import create_movie_suggestion_chain
from core.chain_details import create_movie_details_chain


def create_movie_analysis_graph():
    """
    Orquestra múltiplas chains para criar um grafo que analisa filmes por gênero.
    """
    suggestion_chain = create_movie_suggestion_chain()
    details_chain = create_movie_details_chain()

    def extract_titles_for_mapping(input_dict: dict) -> List[Dict[str, str]]:
        """
        Pega o dicionário de estado, extrai a lista de filmes
        e a prepara para o .map() da próxima chain.
        """
        movie_list: MovieList = input_dict["suggestion_result"]
        return [{"movie_title": title} for title in movie_list.movies]

    # --- AQUI ESTÁ A MUDANÇA PRINCIPAL ---
    # Nós definimos um dicionário inicial que representa o 'estado' do nosso grafo.
    # A suggestion_chain agora é chamada DENTRO do RunnablePassthrough.assign
    # para criar uma nova chave no estado, em vez de substituir o estado inteiro.
    final_graph = RunnablePassthrough.assign(
        # 1. Cria a chave 'suggestion_result' executando a suggestion_chain.
        #    O 'RunnablePassthrough()' inicial garante que o input `{genre: ...}`
        #    seja passado para a suggestion_chain.
        suggestion_result=suggestion_chain,
    ).assign(
        # 2. Agora, com o estado contendo 'suggestion_result', criamos a
        #    chave 'detailed_results' usando essa informação.
        detailed_results=(
            extract_titles_for_mapping  # Recebe todo o dicionário de estado
            | details_chain.map()
        )
    )

    return final_graph #type: ignore