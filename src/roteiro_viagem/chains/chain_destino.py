"""Chain - Destino
A partir do interesse do usuário, a chain retorna uma cidade recomendada.
"""
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models.pydantic_models import Destino
from utils.logger_setup import project_logger  # Loguru

if TYPE_CHECKING:
    from langchain_core.runnables import Runnable


def create_chain_destino(model: ChatOpenAI) -> Callable[[dict[str, Any]], Destino]:
    """Cria uma chain que, a partir do interesse de atividade do usuário,
    recomenda uma cidade ou região no Brasil ou no mundo onde essa atividade
    seja especialmente atrativa, justificando a escolha.
    """
    parser = JsonOutputParser(pydantic_object=Destino)

    prompt = ChatPromptTemplate.from_template(
        """
        O usuário informou um interesse principal de atividade: "{interesse}".
        Sua tarefa é recomendar uma cidade ou região onde essa atividade
        seja muito popular e bem estruturada, levando em conta:

        - Condições naturais ou urbanas ideais para a prática
        - Presença de infraestrutura turística
        - Segurança e facilidade de acesso
        - Atratividade geral do destino

        Responda apenas com um objeto JSON no formato especificado.
        Inclua:
        - "cidade": nome da cidade ou região recomendada
        - "motivo": breve explicação (2-4 frases) justificando a escolha

        {format_instructions}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Cria a chain usando o operador pipe
    chain: Runnable[dict[str, Any], Destino] = prompt | model | parser

    # Função que intercepta entrada e saída para log
    def run_with_logging(inputs: dict[str, Any]) -> Destino:
        project_logger.debug(f"[Chain Destino] Entrada recebida: {inputs}")
        output = chain.invoke(inputs)
        project_logger.debug(f"[Chain Destino] Saída gerada: {output}")
        return output

    return run_with_logging
