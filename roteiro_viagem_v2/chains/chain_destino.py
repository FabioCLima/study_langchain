"""
Chain - Destino
A partir do interesse do usuário, a chain retorna uma cidade recomendada.
"""
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable
from models.pydantic_models import Destino

def create_chain_destino(model: ChatOpenAI) -> Runnable[Dict[str, Any], Destino]:
    
    parser = JsonOutputParser(pydantic_object=Destino)
    prompt = ChatPromptTemplate.from_template(
        """Sugira uma cidade com base no interesse do usuário: {interesse}
        Explique o motivo da sugestão da cidade.
        
        {format_instructions}""",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    return prompt | model | parser
