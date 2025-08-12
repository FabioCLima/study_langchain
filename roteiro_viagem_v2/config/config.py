# roteiro_viagem_v2/config.py
"""
Configuração de variáveis do projeto.

Este módulo gerencia todas as configurações do projeto usando Pydantic para validação
de tipos e carregamento automático de variáveis de ambiente.

Exemplo de uso:
    from config import settings

    # Acessar configurações básicas
    model_name = settings.model_name
    temperature = settings.temperature

    # Acessar chaves secretas (sempre use get_secret_value())
    openai_key = settings.openai_api_key.get_secret_value()
    langchain_key = settings.langchain_api_key.get_secret_value()

    # Usar em aplicações LangChain
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        model_name=settings.model_name,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens
    )
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações do projeto com validação automática de tipos.

    Esta classe herda de BaseSettings do Pydantic, permitindo carregamento
    automático de variáveis de ambiente e validação de tipos.

    Attributes:
        openai_api_key (SecretStr): Chave da API OpenAI (obrigatória)
        langchain_api_key (SecretStr): Chave da API LangChain (obrigatória)
        langchain_project (str): Nome do projeto LangChain (padrão: "roteiro_viagem_v2")
        model_name (str): Nome do modelo GPT a ser usado (padrão: "gpt-4.1")
        temperature (float): Temperatura para geração de texto (padrão: 0.3)
        max_tokens (int): Número máximo de tokens na resposta (padrão: 1024)

    Example:
        # Carregar configurações automaticamente do arquivo .env
        settings = Settings()

        # Acessar valores
        print(f"Modelo: {settings.model_name}")
        print(f"Temperatura: {settings.temperature}")

        # Para chaves secretas, sempre use get_secret_value()
        api_key = settings.openai_api_key.get_secret_value()

        # Sobrescrever valores via variáveis de ambiente
        # export OPENAI_API_KEY="sk-..."
        # export TEMPERATURE="0.7"
    """

    openai_api_key: SecretStr
    """Chave da API OpenAI. Deve ser definida no arquivo .env ou variável de ambiente."""

    langchain_api_key: SecretStr
    """Chave da API LangChain. Deve ser definida no arquivo .env ou variável de ambiente."""

    langchain_project: str = "roteiro_viagem_v2"
    """Nome do projeto LangChain. Padrão: 'roteiro_viagem_v2'."""

    model_name: str = "gpt-4.1"
    """Nome do modelo GPT a ser usado. Padrão: 'gpt-4.1'."""

    temperature: float = 0.3
    """
    Temperatura para geração de texto.
    
    Valores mais baixos (0.1-0.3) produzem respostas mais determinísticas.
    Valores mais altos (0.7-1.0) produzem respostas mais criativas.
    Padrão: 0.3
    """

    max_tokens: int = 1024
    """
    Número máximo de tokens na resposta.
    
    Um token é aproximadamente 4 caracteres em português.
    Limite recomendado: 1024-4096 para respostas concisas.
    Padrão: 1024
    """

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
    """
    Configurações do modelo Pydantic.
    
    - env_file: Arquivo .env para carregar variáveis de ambiente
    - env_file_encoding: Codificação do arquivo .env (UTF-8)
    """


# Instância global das configurações
# Parte do código pode ler settings.model_name
settings = Settings()  # type: ignore
