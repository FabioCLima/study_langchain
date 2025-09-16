"""Chain - Passeios Culturais
A partir da cidade recomendada, a chain retorna uma lista de passeios culturais.
"""
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models.pydantic_models import ListaAtracoes
from utils.logger_setup import project_logger  # Loguru

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable


def create_chain_passeios_culturais(model: ChatOpenAI) -> Callable[[dict[str, Any]], ListaAtracoes]:
    """Cria uma chain que, a partir de uma cidade, retorna uma lista de passeios culturais,
    formatada de acordo com o modelo Pydantic ListaAtracoes.
    """
    parser = PydanticOutputParser(pydantic_object=ListaAtracoes)

    prompt = ChatPromptTemplate.from_template(
        """
        Sugira 3 passeios culturais na cidade {cidade}.
        Para cada passeio, forneça:
        - nome: nome do passeio
        - descricao: descrição detalhada do passeio

        {format_instructions}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain: Runnable[dict[str, Any], ListaAtracoes] = prompt | model | parser

    def run_with_logging(inputs: dict[str, Any]) -> ListaAtracoes:
        project_logger.debug(f"[Chain Passeios] Entrada recebida: {inputs}")
        output = chain.invoke(inputs)
        project_logger.debug(f"[Chain Passeios] Saída gerada: {output}")
        return output

    return run_with_logging
