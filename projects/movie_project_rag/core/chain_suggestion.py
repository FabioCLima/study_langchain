# core/chain_suggestion.py

from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from core.models import MovieList
from core.settings import settings


def create_movie_suggestion_chain() -> Runnable[dict[str, Any], MovieList]:
    """Cria e retorna uma chain que sugere filmes de um gênero específico."""
    llm = ChatOpenAI(model=settings.model_name, temperature=settings.model_temperature)
    prompt_template = ChatPromptTemplate([
        ("system", "Você é um especialista em cinema..."),
        ("human", "Por favor, me recomende uma lista de 10 filmes excelentes do gênero '{genre}'. Liste apenas os títulos dos filmes."),
    ])
    structured_llm = llm.with_structured_output(MovieList)  # type: ignore
    chain = prompt_template | structured_llm  # type: ignore
    return chain  # type: ignore
