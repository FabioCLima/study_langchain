"""
Knowledge Boundary Agent using Structured Output
"""
from ..core.state import AgentState
from ..core.settings import get_llm_factory
from ..core.prompts import boundary_check_prompt
from ..core.models import ScopeDecision

def boundary_check_node(state: AgentState) -> str:
    """
    Checks if the enhanced question is within scope using structured output.
    """
    print("--- 🚪 EXECUTANDO NÓ: Validador de Domínio (Estruturado) ---")

    enhanced_question = state["enhanced_question"]
    specialization = state["specialization"]

    llm_factory = get_llm_factory()
    boundary_llm = llm_factory.create_llm(temperature=0.0)
    
    structured_llm = boundary_llm.with_structured_output(ScopeDecision)
    boundary_chain = boundary_check_prompt | structured_llm

    decision_result = boundary_chain.invoke({
        "question": enhanced_question,
        "specialization": specialization
    })

    is_in_scope = decision_result.is_in_scope
    print(f"A pergunta está no escopo de '{specialization}'? -> {is_in_scope}")

    if is_in_scope:
        return "in_scope"
    else:
        return "out_of_scope"