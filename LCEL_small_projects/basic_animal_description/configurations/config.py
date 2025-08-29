'''Centraliza as configurações do projeto'''

import os
from dotenv import find_dotenv, load_dotenv
from pydantic import SecretStr
from langchain_openai import ChatOpenAI


#* Desabilita o tracing para manter o output limpo nos exercícios
os.environ["LANGCHAIN_TRACING_V2"] = "false"


#* Carregar as variáveis de ambiente
_ = load_dotenv(find_dotenv())

#* Valida se a chave da API foi carregada
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    error_msg = "A chave da API não foi carregada."
    raise ValueError(error_msg)

#* Instancia central do LLM
api_openai_key = os.getenv("OPENAI_API_KEY")
if not api_openai_key:
    error_msg = "A chave da API não foi carregada."
    raise ValueError(error_msg)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=SecretStr(api_openai_key),
)
