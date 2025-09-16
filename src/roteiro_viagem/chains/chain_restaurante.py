"""Chain - Restaurantes
A partir da cidade recomendada, a chain retorna uma lista de restaurantes.
"""
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models.pydantic_models import ListaRestaurantes
from utils.logger_setup import project_logger  # Loguru

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable


def create_chain_restaurantes(model: ChatOpenAI) -> Callable[[dict[str, Any]], ListaRestaurantes]:
    """Cria uma chain que, dada uma cidade, sugere uma lista de restaurantes
    formatada de acordo com o modelo Pydantic ListaRestaurantes.
    """
    parser = PydanticOutputParser(pydantic_object=ListaRestaurantes)

    prompt_template = """
    Você é um assistente especialista em gastronomia e trabalha para uma agência de viagens.

    Para a cidade {cidade}, sugira uma lista contendo:
    - 3 restaurantes de comida caseira de boa qualidade
    - 3 restaurantes mais sofisticados

    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain: Runnable[dict[str, Any], ListaRestaurantes] = prompt | model | parser

    def run_with_logging(inputs: dict[str, Any]) -> ListaRestaurantes:
        project_logger.debug(f"[Chain Restaurantes] Entrada recebida: {inputs}")
        output = chain.invoke(inputs)
        project_logger.debug(f"[Chain Restaurantes] Saída gerada: {output}")
        return output

    return run_with_logging
