"""Exercício simples de chain"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser  # type: ignore
from langchain_core.prompts import ChatPromptTemplate  # type: ignore
from langchain_openai import ChatOpenAI  # type: ignore

# Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Verifica se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

# Configura o modelo com parâmetros específicos
model: ChatOpenAI = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,  # Controla a criatividade das respostas
)  # type: ignore

prompt = ChatPromptTemplate.from_template(
    "Crie uma frase sobre o seguinte tema: {assunto}"
)
parser = StrOutputParser()

chain = prompt | model | parser  # type: ignore

try:
    response = chain.invoke({"assunto": "LangChain"})  # type: ignore
    print(response)
except Exception as e:
    print(f"Erro ao executar a chain: {e}")
