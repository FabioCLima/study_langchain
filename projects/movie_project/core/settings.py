# core/settings.py

import os
from pathlib import Path

from dotenv import find_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Carrega e valida as configurações do projeto a partir de um arquivo .env."""

    # --- Configurações Gerais ---
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    output_dir: Path = Field(default=BASE_DIR / "data")

    # --- Chaves de API ---
    openai_api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")

    # --- LangSmith (Opcional) ---
    langchain_tracing_v2: bool = Field(default=True, alias="LANGCHAIN_TRACING_V2")
    langchain_endpoint: str = Field(
        default="https://api.smith.langchain.com", alias="LANGCHAIN_ENDPOINT"
    )
    langchain_api_key: SecretStr | None = Field(
        default=None, alias="LANGCHAIN_API_KEY"
    )
    langchain_project: str | None = Field(
        default="Langchain Movies Project", alias="LANGCHAIN_PROJECT"
    )

    # --- Configurações do Modelo LLM ---
    model_name: str = Field(default="gpt-4o-mini", alias="MODEL_NAME")
    model_temperature: float = Field(default=0.3, alias="MODEL_TEMPERATURE")

    model_config = SettingsConfigDict(
        env_file=find_dotenv(), env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()  # type: ignore[call-arg]

settings.output_dir.mkdir(parents=True, exist_ok=True)


def setup_environment() -> None:
    """Configura as variáveis de ambiente necessárias para OpenAI e LangSmith
    a partir do objeto de settings já carregado.
    """
    # --- Configuração da OpenAI ---
    if settings.openai_api_key:
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key.get_secret_value()

    # --- Configuração do LangSmith ---
    if settings.langchain_api_key:
        from core.logger import logger  # noqa: PLC0415

        os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2)
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
        os.environ["LANGCHAIN_API_KEY"] = (
            settings.langchain_api_key.get_secret_value()
        )

        if settings.langchain_project:
            os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
            logger.info(
                "LangSmith tracing habilitado para o projeto: '%s'",
                settings.langchain_project,
            )
        else:
            logger.warning(
                "LangSmith API Key encontrada, mas nenhum projeto foi definido."
            )
