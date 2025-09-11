"""Construção das chains e pipeline final.

Exporta:
    build_pipeline() -> final_chain (runnable)
"""

from collections.abc import Mapping
from typing import Any

from country_capital_proj.config import settings
from country_capital_proj.models import Curiosidade, Pais, ResultadoFinal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI


def _build_country_chain() -> Runnable:
    """Chain que recebe 'pais' e retorna um objeto Pais (with_structured_output)."""
    model_pais = ChatOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        model=settings.model_pais_name,
        temperature=settings.model_pais_temp,
    ).with_structured_output(Pais)

    prompt_pais = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente que sabe informações sobre países."),
            ("user", "Qual é a capital do {pais}?"),
        ]
    )

    return prompt_pais | model_pais


def _build_city_chain() -> Runnable:
    """Chain que recebe 'cidade' e retorna um objeto Curiosidade (with_structured_output)."""
    model_city = ChatOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        model=settings.model_city_name,
        temperature=settings.model_city_temp,
    ).with_structured_output(Curiosidade)

    prompt_city = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente que sabe informações sobre cidades."),
            (
                "user",
                "Responda APENAS em JSON com a chave 'curiosidade'. "
                "Diga uma curiosidade curta sobre a cidade {cidade}.",
            ),
        ]
    )

    return prompt_city | model_city


def extract_city_from_country(data: Mapping[str, Any]) -> dict[str, str]:
    """Extrai a cidade (capital) do país para passar como entrada na chain da cidade.

    Args:
        data: dicionário contendo a chave 'pais_obj' (resultado do chain_pais).

    Returns:
        dict: {"cidade": <capital>}

    """
    # pais_obj vem como uma instância Pydantic (Pais) quando usamos
    # with_structured_output
    pais_obj = data["pais_obj"]
    return {"cidade": pais_obj.capital}


def build_final_result(data: Mapping[str, Any]) -> ResultadoFinal:
    """Monta a saída final estruturada da pipeline.

    Args:
        data: dicionário contendo 'pais_obj' (Pais) e 'curiosity_city' (Curiosidade).

    Returns:
        ResultadoFinal: saída tipada com país, capital e curiosidade.

    """
    pais_obj = data["pais_obj"]
    curiosity_obj = data["curiosity_city"]
    return ResultadoFinal(
        pais=pais_obj.nome,
        capital=pais_obj.capital,
        curiosidade=curiosity_obj.curiosidade,
    )


def build_pipeline() -> Runnable:
    """Constrói e retorna a pipeline final (runnable)."""
    chain_pais = _build_country_chain()
    chain_city = _build_city_chain()

    sub_chain_city = RunnableLambda(extract_city_from_country) | chain_city

    return (
        RunnablePassthrough.assign(pais_obj=chain_pais)
        | RunnablePassthrough.assign(curiosity_city=sub_chain_city)
        | RunnableLambda(build_final_result)
    )
