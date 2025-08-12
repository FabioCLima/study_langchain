# utils/llm_setup.py
from typing import Optional, Union
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from config.config import settings # type: ignore


def create_model(api_key: Optional[Union[str, SecretStr]] = None) -> ChatOpenAI:
    """Cria e configura uma instância do modelo ChatOpenAI.

    Utiliza as configurações globais do projeto (como nome do modelo, temperatura)
    e permite a sobreposição da chave de API.

    Args:
        api_key: Opcional. A chave da API da OpenAI. Pode ser uma string
            ou um objeto SecretStr. Se não for fornecida, utiliza a
            chave definida nas configurações do projeto.

    Returns:
        Uma instância configurada de ChatOpenAI.
    """
    # Define qual chave de API será usada, priorizando a que foi passada como argumento.
    key_to_use = api_key if api_key is not None else settings.openai_api_key

    # O construtor do ChatOpenAI espera um objeto SecretStr.
    # Esta conversão garante que o tipo correto seja sempre passado.
    if isinstance(key_to_use, str):
        key_to_use = SecretStr(key_to_use)

    return ChatOpenAI(
        model=settings.model_name,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens, #type: ignore
        api_key=key_to_use,
    )
