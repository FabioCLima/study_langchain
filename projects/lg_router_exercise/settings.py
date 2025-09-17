# settings.py
"""Módulo de Configurações da Aplicação.

Este módulo é responsável por carregar, validar e fornecer acesso às
configurações da aplicação de forma centralizada. Ele utiliza a biblioteca
Pydantic para validar as configurações a partir de variáveis de ambiente
(carregadas de um arquivo .env) e garante que uma única instância
dessas configurações seja usada em toda a aplicação (padrão Singleton
implementado com @lru_cache).

O módulo também inclui tratamento de erros para garantir que a aplicação
falhe de forma clara e informativa se as configurações essenciais não
forem encontradas.
"""

import sys
from functools import lru_cache

from dotenv import load_dotenv
from loguru import logger
from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações essenciais para execução do grafo e tracing com LangSmith."""

    langsmith_api_key: SecretStr = Field(
        ..., description="Chave da API do LangSmith (obrigatória para tracing)"
    )
    langsmith_project: str = Field(
        default="LangGraph - String Processor",
        description="Nome do projeto no LangSmith",
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Carrega, valida e retorna a instância global das configurações.

    Na primeira chamada, carrega as variáveis de ambiente e tenta instanciar
    as configurações. Em caso de falha de validação (ex: variável faltando
    no .env), um erro crítico é logado e a aplicação é encerrada.

    Returns:
        Settings: A instância única e global das configurações da aplicação.

    """
    load_dotenv()  # Carrega variáveis de ambiente do arquivo .env
    try:
        return Settings()
    except ValidationError as e:
        logger.critical(
            "❌ Falha ao carregar as configurações da aplicação. "
            "Verifique se o arquivo .env existe e contém todas as "
            "variáveis obrigatórias.\nDetalhes do Erro:\n{error}",
            error=e,
        )
        # Encerra a aplicação, pois ela não pode funcionar sem as configs.
        sys.exit(1)
