"""
Specialist Agent Node
=====================
This module contains the node for generating an expert response.
"""
from langchain_core.output_parsers import StrOutputParser

from ..core.state import AgentState
from ..core.settings import get_llm_factory
# A correção está aqui: importamos a variável correta de prompts.py
from ..core.prompts import specialist_chat_prompt

def specialist_node(state: AgentState) -> dict[str, str]:
    """
    Generates a final answer using a ChatPromptTemplate.
    """
    print("--- 🧑‍🏫 EXECUTANDO NÓ: Gerar Resposta do Especialista ---")

    enhanced_question = state["enhanced_question"]
    specialization = state["specialization"]

    llm_factory = get_llm_factory()
    specialist_llm = llm_factory.create_specialist_llm()
    
    # A chain agora usa o ChatPromptTemplate importado
    chain = specialist_chat_prompt | specialist_llm | StrOutputParser()

    final_answer = chain.invoke({
        "question": enhanced_question,
        "specialization": specialization
    })

    return {"answer": final_answer}