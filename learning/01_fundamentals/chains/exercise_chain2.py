"""Exercício: Chain que aceita múltiplas entradas
"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# * Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# * Verifica se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

model: ChatOpenAI = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
)

# * Template com múltiplas entradas
prompt = ChatPromptTemplate.from_template(
    """
    Você é um {role} especializado em {subject}.
    Responda a seguinte pergunta de forma {style}:
    
    Pergunta: {question}
    """
)
output_parser = StrOutputParser()

chain = prompt | model | output_parser

response = chain.invoke(
    {
        "role": "professor",
        "subject": "Python",
        "style": "didática e simples",
        "question": "o que é um decorador em Python?",
    }
)

print(response)
