"""Main Workflow Definition for the Assistant Questions Project
============================================================

This module defines and compiles the LangGraph, exporting the final 'app' object.
It acts as the "factory" for our workflow.
"""

from langgraph.graph import END, StateGraph

from ..agents.knowledge_boundary import boundary_check_node
from ..agents.question_enhancer import enhance_question_node
from ..agents.specialist_agent import specialist_node
from ..core.state import AgentState


def out_of_scope_node(state: AgentState) -> dict[str, str]:
    print("--- 🚫 EXECUTANDO NÓ: Fora de Escopo ---")
    specialization = state["specialization"]
    answer = f"Desculpe, a pergunta aprimorada parece estar fora da minha área de especialização em '{specialization}'. Por favor, faça uma pergunta relacionada ao tema."
    return {"answer": answer}


workflow = StateGraph(AgentState)

workflow.add_node("enhancer", enhance_question_node)
workflow.add_node("specialist", specialist_node)
workflow.add_node("out_of_scope", out_of_scope_node)

workflow.set_entry_point("enhancer")
workflow.add_conditional_edges(
    "enhancer",
    boundary_check_node,
    {"in_scope": "specialist", "out_of_scope": "out_of_scope"},
)
workflow.add_edge("specialist", END)
workflow.add_edge("out_of_scope", END)

app = workflow.compile()
