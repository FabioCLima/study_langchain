"""Exercício: Simple Chain

formata uma pergunta e a envia para um LLM

Requisitos:
- LangChain
- LangChain-OpenAI
- OpenAI
"""

import os
from typing import Any

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser  # type: ignore
from langchain_core.prompts import ChatPromptTemplate  # type: ignore
from langchain_core.runnables import RunnableSerializable  # type: ignore
from langchain_openai import ChatOpenAI  # type: ignore

# * Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# * Verifica se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

# * Configura o modelo com parâmetros específicos
model: ChatOpenAI = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,  # Controla a criatividade das respostas
)  # type: ignore

# * Configuração básica
prompt = ChatPromptTemplate.from_template(
    "Você é um assistente útil. Responda a pergunta: {question}"
)
output_parser = StrOutputParser()

# * Chain usando LCEL
chain: RunnableSerializable[dict[str, Any], str] = prompt | model | output_parser  # type: ignore
response: str = chain.invoke({"question": "O que é inteligência artificial?"})  # type: ignore
print(response)
