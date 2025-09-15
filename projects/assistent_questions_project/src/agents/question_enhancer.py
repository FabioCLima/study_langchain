"""
Question Enhancer Agent
=======================

This module contains the node for enhancing user questions.
"""
# Não precisamos mais do StrOutputParser, pois a saída será um objeto Pydantic
# from langchain_core.output_parsers import StrOutputParser

from ..core.state import AgentState
from ..core.settings import get_llm_factory
from ..core.prompts import enhancer_prompt
from ..core.models import EnhancedQuestion # <-- Importar nosso novo modelo

def enhance_question_node(state: AgentState) -> dict[str, str]:
    """
    Enhances the user's original question using structured output.
    """
    print("--- 🧠 EXECUTANDO NÓ: Aprimorar Pergunta (com Saída Estruturada) ---")
    
    original_question = state["original_question"]
    specialization = state["specialization"]
    
    llm_factory = get_llm_factory()
    # Usamos o create_llm normal e adicionamos a lógica de structured output
    enhancer_llm = llm_factory.create_llm(temperature=0.1)
    
    # É AQUI QUE A MÁGICA ACONTECE
    # Forçamos o LLM a preencher nosso modelo EnhancedQuestion
    structured_llm = enhancer_llm.with_structured_output(EnhancedQuestion)
    
    # A chain agora retorna um objeto EnhancedQuestion, não mais uma string
    enhancer_chain = enhancer_prompt | structured_llm
    
    # Executamos a chain
    enhancement_result = enhancer_chain.invoke({
        "question": original_question,
        "specialization": specialization
    })
    
    # Extraímos a string limpa do objeto de resultado
    clean_enhanced_question = enhancement_result.enhanced_question
    
    print(f"Original: '{original_question}'")
    print(f"Aprimorada (Limpa): '{clean_enhanced_question}'")
    
    return {"enhanced_question": clean_enhanced_question}