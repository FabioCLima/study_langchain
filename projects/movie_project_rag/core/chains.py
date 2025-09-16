# pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false
"""Módulo responsável por construir e expor as chains LangChain do projeto.
"""

from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from core.models import MovieInfoData, MovieList
from core.settings import settings


def create_movie_suggestion_chain() -> Runnable[dict[str, Any], MovieList]:
    """Cria e retorna uma chain que sugere filmes de um gênero específico,
    estruturando a saída no modelo MovieList.
    """
    llm = ChatOpenAI(
        model=settings.model_name,
        temperature=settings.model_temperature,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Você é um especialista em cinema com conhecimento enciclopédico sobre filmes de todos os gêneros e épocas. Sua paixão é recomendar filmes de alta qualidade para os outros.",
            ),
            (
                "human",
                "Por favor, me recomende uma lista de 10 filmes excelentes do gênero '{genre}'. Liste apenas os títulos dos filmes.",
            ),
        ]
    )

    # Com o Pyright instruído a ignorar os erros, não precisamos mais do 'cast'
    # ou de anotações complexas aqui dentro. O código fica mais limpo.
    structured_llm = llm.with_structured_output(MovieList)  # type: ignore

    chain = prompt_template | structured_llm  # type: ignore

    return chain  # type: ignore

# Adicione esta função ao seu core/chains.py


def create_movie_details_chain() -> Runnable[dict[str, Any], MovieInfoData]:
    """Cria uma chain que recebe o título de um filme e retorna
    informações detalhadas sobre ele, usando o modelo MovieInfoData.
    """
    llm = ChatOpenAI(
        model=settings.model_name,
        temperature=settings.model_temperature,
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Você é um assistente de banco de dados de cinema. Sua função é receber o título de um filme e preencher de forma precisa e concisa as informações sobre ele.",
            ),
            (
                "human",
                "Por favor, extraia as seguintes informações para o filme: '{movie_title}'.",
            ),
        ]
    )

    structured_llm = llm.with_structured_output(MovieInfoData)  # type: ignore
    details_chain = prompt_template | structured_llm  # type: ignore
    return details_chain  # type: ignore
