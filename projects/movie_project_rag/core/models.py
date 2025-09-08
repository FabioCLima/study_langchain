# core/models.py
"""
Módulo para definir as estruturas de dados (modelos Pydantic) do projeto.

Estes modelos são usados para garantir que a saída do LLM seja estruturada,
confiável e fácil de usar no restante da aplicação.
"""

from typing import List
from pydantic import BaseModel, Field


class MovieList(BaseModel):
    """
    Um modelo de dados que representa uma lista simples de títulos de filmes.
    Este é o nosso primeiro modelo, focado apenas em obter os nomes.
    """

    movies: List[str] = Field(
        ...,
        description=(
            "Uma lista contendo os títulos dos filmes. "
            "Exemplo: ['O Senhor dos Anéis', 'Matrix', 'Interestelar']"
        ),
    )

# --- NOSSO NOVO MODELO DE DADOS ---
class MovieInfoData(BaseModel):
    """
    Estrutura de dados para armazenar informações detalhadas sobre um único filme.
    """
    title: str = Field(..., description="O título oficial do filme.")

    director: str = Field(..., description="O nome do diretor principal do filme.")

    main_actors: List[str] = Field(
        ..., description="Uma lista com os nomes dos 3 a 5 atores principais."
    )

    release_year: int = Field(..., description="O ano de lançamento do filme.")

    box_office_revenue: float = Field(
        ...,
        description="A receita total de bilheteria mundial em dólares americanos.",
    )

    oscars_won: int = Field(
        ..., description="O número total de prêmios Oscar que o filme ganhou."
    )

#! --- NOVOS MODELOS PARA GERAÇÃO DO CATÁLOGO ---

class Filme(BaseModel):
    """
    Modelo Pydantic para representar a estrutura de um único filme no catálogo.
    """
    title: str = Field(description="O título original ou mais conhecido do filme.")
    synopsis: str = Field(description="Uma sinopse concisa do filme, com 2 a 3 frases, destacando o enredo principal e o gênero.")

class CatalogoFilmes(BaseModel):
    """
    Modelo Pydantic que encapsula uma lista de filmes, representando o catálogo completo.
    """
    filmes: List[Filme] = Field(description="Uma lista contendo múltiplos objetos de filmes.")