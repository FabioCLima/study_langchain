"""Crie uma chain que recebe o nome de um animal e retorna uma descrição básica sobre ele."""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr

# * Carregar as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# * Valida se a chave da API foi carregada
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    error_msg = "A chave da API não foi carregada."
    raise ValueError(error_msg)


# --- Modelos de Dados Pydantic ---
class AnimalNome(BaseModel):
    """Representa apenas o nome de um animal."""

    nome: str = Field(description="O nome do animal.")


class AnimalDescricao(BaseModel):
    """Representa a descrição de um animal."""

    nome: str = Field(description="O nome do animal.")
    descricao: str = Field(description="Uma descrição curta sobre o animal.")


# --- Instancia Central do LLM ---
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    api_key=SecretStr(api_key),
)
print("Módulo 'utils' carregado com sucesso. LLM configurado")
