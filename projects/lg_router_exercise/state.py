# state.py
# state.py
"""Módulo de Definição do Estado do Grafo.

Este módulo contém a definição da estrutura de dados para o estado
do grafo LangGraph, utilizando Pydantic para validação e tipagem clara.
A classe `State` serve como o contêiner central de dados que é passado
entre os nós do fluxo de trabalho de processamento de texto.
"""

from typing import Literal

from pydantic import BaseModel, Field


class State(BaseModel):
    """Define o estado do grafo para o processamento de texto usando Pydantic.

    Esta classe Pydantic serve como o contêiner de dados para o estado
    do grafo LangGraph, garantindo a consistência e a validação dos dados
    que fluem entre os nós.

    Atributos:
        user_string (str): A string de entrada a ser processada.
        action_type (Literal["reverse", "upper"]): O tipo de operação a ser realizada.
        processed_string (str): A string resultante após a execução de um nó de
        processamento.

    Exemplo de uso no fluxo:
        # 1. Estado inicial antes da execução do grafo
        >>> estado_inicial = State(
        ...     user_string="Hello World",
        ...     action_type="reverse"
        ... )

        # 2. Após a execução do nó 'reverse_node', o estado é atualizado
        # >>> estado_final = grafo.invoke(estado_inicial)
        # >>> print(estado_final.processed_string)
        # "dlroW olleH"

    Nota:
        O uso de `Literal` para `action_type` garante que apenas operações válidas
        sejam passadas. Uma `action_type` inválida resultará em um erro de validação
        do Pydantic antes mesmo de chegar ao roteador do grafo, tornando o fluxo
        mais seguro e previsível.
    """

    user_string: str = Field(description="A string de entrada a ser processada.")

    action_type: Literal["reverse", "upper"] = Field(
        description="O tipo de operação a ser realizada na string."
    )

    processed_string: str = Field(
        default="", description="A string resultante após o processamento."
    )
