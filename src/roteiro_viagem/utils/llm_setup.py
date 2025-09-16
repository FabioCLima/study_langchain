"""Carregando variáveis de ambiente e configurando o modelo de linguagem"""

import os
from typing import cast

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def load_environment_variables() -> SecretStr:
    """Carrega a chave da API do OpenAI das variáveis de ambiente.
    
    Returns:
        SecretStr: A chave da API do OpenAI como SecretStr
        
    Raises:
        ValueError: Se a chave da API não for encontrada

    """
    load_dotenv(find_dotenv())
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
    return SecretStr(api_key)


def create_model(api_key: str | SecretStr) -> ChatOpenAI:
    """Cria uma instância do modelo ChatOpenAI.
    
    Args:
        api_key: A chave da API do OpenAI (str ou SecretStr)
        
    Returns:
        ChatOpenAI: Instância configurada do modelo

    """
    if isinstance(api_key, str):
        api_key = SecretStr(api_key)
    return ChatOpenAI(model="gpt-4o", api_key=api_key)


if __name__ == "__main__":
    """Exemplo de uso do módulo."""
    try:
        openai_api_key = load_environment_variables()
        model = create_model(openai_api_key)
        response = model.invoke("Qual é o local onde surgiu a primeira civilização??")
        print(cast("str", response.content))
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
