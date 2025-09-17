# nodes.py
"""Módulo com os nós de processamento e a lógica de roteamento do grafo.

Este arquivo contém todas as funções que atuam como "etapas" (nós) no
fluxo de trabalho do LangGraph. Cada nó recebe o estado atual do grafo,
executa uma tarefa específica e retorna um dicionário com as atualizações
para o estado.

Inclui também a função de roteamento (`router`) que direciona o fluxo
para o nó apropriado com base no `action_type` definido no estado.
"""

from loguru import logger

from .state import State


def reverse_node(state: State) -> dict[str, str]:
    """Inverte a string contida em `state.user_string`.

    Args:
        state: A instância Pydantic atual do estado do grafo.

    Returns:
        Um dicionário contendo a chave `processed_string` com o
        resultado da operação para que o LangGraph atualize o estado.

    Exemplo:
        # Supondo que o estado contenha:
        # state.user_string = "hello world"
        # O retorno será:
        # {"processed_string": "dlrow olleh"}

    """
    logger.info("--- 🔄 REVERSE NODE ---")

    # * 1. Acessa o estado como um atributo de objeto
    input_string = state.user_string
    logger.debug(f"String de entrada: {input_string}")

    # * 2. Executa a lógica principal
    reversed_string = input_string[::-1]
    logger.debug(f"String processada: {reversed_string}")

    # * 3. Retorna um dicionário apenas com o campo que foi alterado
    logger.success("Nó de reversão concluído.")
    return {"processed_string": reversed_string}


def upper_node(state: State) -> dict[str, str]:
    """Converta a string em `state.user_string` para maiúsculas.

    Args:
        state: A instância Pydantic atual do estado do grafo.

    Returns:
        Um dicionário contendo a chave `processed_string` com o
        resultado da operação para que o LangGraph atualize o estado.

    Exemplo:
        # Supondo que o estado contenha:
        # state.user_string = "hello world"
        # O retorno será:
        # {"processed_string": "HELLO WORLD"}

    """
    logger.info("--- ⬆️ EXECUTANDO NÓ DE CAPITALIZAÇÃO ---")

    # Acessa o estado como um atributo de objeto
    input_string = state.user_string
    logger.debug(f"String de entrada: {input_string}")

    # Executa a lógica principal
    upper_string = input_string.upper()
    logger.debug(f"String processada: {upper_string}")

    # Retorna um dicionário apenas com o campo que foi alterado
    logger.success("Nó de capitalização concluído.")
    return {"processed_string": upper_string}


# Em nodes.py


def router(state: State) -> str:
    """Determine o próximo nó a ser executado com base na ação definida no estado.

    Esta função atua como a aresta condicional principal do grafo. Ela lê
    o atributo `action_type` do estado e retorna o nome do nó correspondente
    para a próxima etapa do fluxo de trabalho.

    Args:
        state (State): A instância Pydantic atual do estado do grafo,
            contendo o `action_type` para roteamento.

    Returns:
        str: O nome do próximo nó a ser executado ("reverse_node" ou "upper_node").

    Raises:
        ValueError: Lançada se o `action_type` no estado não for um dos
            valores esperados.

    """
    logger.info(f"---🧭 ROTEADOR: Decidindo rota para a ação '{state.action_type}'---")

    # * Não precisamos verificar se a ação existe ou é válida.
    # * Pydantic já garantiu isso para nós!
    if state.action_type == "reverse":
        return "reverse_node"
    if state.action_type == "upper":
        return "upper_node"

    # Esta é a versão que satisfaz todas as regras do ruff (TRY003 e EM101)
    error_message = "Ação desconhecida"
    raise ValueError(error_message, state.action_type)
