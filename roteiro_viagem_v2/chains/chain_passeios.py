''' Chain - Passeios Culturais
A partir da cidade recomendada, a chain retorna uma lista de passeios culturais.
'''

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

def create_chain_passeios_culturais(model: ChatOpenAI) -> Runnable:
    
    parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_template(
        """Sugira 3 passeios culturais na cidade {cidade}.
        Inclua nome e descrição para cada passeio.
        
        Formato da resposta:
        - Nome do passeio 1: Descrição detalhada
        - Nome do passeio 2: Descrição detalhada  
        - Nome do passeio 3: Descrição detalhada"""
    )
    return prompt | model | parser
