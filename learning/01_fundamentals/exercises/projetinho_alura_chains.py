"""Projeto de langchain - Alura"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

_ = load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    MSG = "OPENAI_API_KEY não encontrada no .env"
    raise ValueError(MSG)

model = ChatOpenAI(model="gpt-4.1", temperature=0.5)

# Versão melhorada:
# 1. Usamos `ChatPromptTemplate.from_template` que é mais moderno e infere
#    as `input_variables` automaticamente. É ideal para `ChatOpenAI`.
# 2. O template foi aprimorado para dar um "papel" (persona) ao modelo,
#    o que geralmente leva a respostas melhores e mais focadas.
# 3. Removemos espaços em branco desnecessários no início do template.
prompt_cidade = ChatPromptTemplate.from_template(
    "Você é um especialista em viagens e turismo. "
    "Sugira uma cidade ideal para alguém com interesse em {interesse}. "
    "Forneça uma sugestão e uma breve justificativa do porquê."
)
parser = StrOutputParser()

chain_interesse = prompt_cidade | model | parser  # type: ignore

response_interesse = chain_interesse.invoke(  # type: ignore
    {"interesse": "cachoeiras"}
)

print(response_interesse)
