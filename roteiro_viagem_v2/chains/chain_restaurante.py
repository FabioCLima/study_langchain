"""
Chain - Restaurantes
A partir da cidade recomendada, a chain retorna uma lista de restaurantes.
"""
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable
from models.pydantic_models import ListaRestaurantes


def create_chain_restaurantes(model: ChatOpenAI) -> Runnable[Dict[str, Any], ListaRestaurantes]:
    """
    Cria e retorna uma chain que, dada uma cidade, sugere uma lista de restaurantes
    formatada de acordo com o modelo Pydantic ListaRestaurantes.
    """
    
    # 1. Criar o Parser:
    # Apenas um parser é necessário. Ele "sabe" como analisar a saída do LLM
    # e como gerar as instruções de formato para o nosso modelo Pydantic.
    parser = PydanticOutputParser(pydantic_object=ListaRestaurantes)

    # 2. Definir o Template do Prompt:
    # Esta é a instrução que damos ao LLM. Note as duas variáveis:
    # {cidade} -> Será preenchida quando executarmos a chain.
    # {format_instructions} -> Será pré-preenchida com as instruções do parser.
    prompt_template = """Você é um assistente especialista em gastronomia e trabalha para a agência de viagens.
    
Para a cidade {cidade}, sugira uma lista contendo:
- 3 restaurantes de comida caseira de boa qualidade
- 3 restaurantes mais sofisticados

{format_instructions}"""

    # 3. Criar o Objeto de Prompt:
    # Usamos o template e já injetamos as instruções de formato.
    # Isso deixa a chain esperando apenas a variável {cidade} no momento da execução.
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # 4. Montar a Chain com o operador pipe (|):
    # Este é o fluxo de dados da LangChain Expression Language (LCEL).
    # O input (dicionário com a "cidade") passa pelo prompt, depois pelo modelo, e finalmente é formatado pelo parser.
    chain = prompt | model | parser
    
    return chain
