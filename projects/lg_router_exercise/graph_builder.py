# graph_builder.py
"""Módulo para a construção e compilação do grafo LangGraph.

Este arquivo contém a lógica para montar o fluxo de trabalho (workflow) do processador de strings. Ele importa o estado e os
nós definidos em outros módulos e os conecta para criar um grafo executável.

A lógica é encapsulada na função `build_graph` para evitar efeitos colaterais
na importação e permitir a instanciação controlada do grafo.
"""

from langgraph.graph import END, StateGraph

from .nodes import reverse_node, upper_node
from .state import State


def build_graph() -> StateGraph:
    """Constrói, conecta e compila o grafo de processamento de strings.

    Returns:
        Um grafo LangGraph compilado e pronto para ser executado.

    """
    grafo = StateGraph(State)

    # * 1. Adiciona os nós que realmente fazem o trabalho (modificam o estado)
    grafo.add_node("reverse_node", reverse_node)
    grafo.add_node("upper_node", upper_node)

    # * 2. Define o ponto de entrada como sendo a própria função de roteamento
    grafo.set_conditional_entry_point(
        # A função que toma a decisão router,
        # O mapeamento de "resultado" -> "nó de destino"
        {
            "reverse_node": "reverse_node",
            "upper_node": "upper_node",
        },
    )

    # 3. Conecta os nós de processamento ao final do fluxo
    grafo.add_edge("reverse_node", END)
    grafo.add_edge("upper_node", END)

    # 4. Compila e retorna o grafo
    return grafo.compile()
