from dotenv import find_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações do projeto carregadas via variáveis de ambiente.

    Esta classe usa pydantic-settings para carregar e validar configurações
    de um arquivo .env.

    Campos obrigatórios (devem estar no .env):
    - OPENAI_API_KEY: Sua chave de API da OpenAI.
    """

    openai_api_key: SecretStr = Field(
        ...,
        alias="OPENAI_API_KEY",
        description="Chave de API da OpenAI para acessar os modelos.",
    )
    langsmith_api_key: SecretStr | None = Field(
        default=None,
        alias="LANGSMITH_API_KEY",
        description="Chave de API do LangSmith para tracing (opcional).",
    )

    langsmith_tracing: bool = Field(
        default=False,
        alias="LANGSMITH_TRACING",
        description="Habilita ou desabilita o tracing com LangSmith.",
    )
    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com",
        alias="LANGSMITH_ENDPOINT",
        description="Endpoint da API do LangSmith.",
    )
    langsmith_project: str = Field(
        default="Langchain studies - FabioLima",
        alias="LANGSMITH_PROJECT",
        description="Nome do projeto no LangSmith.",
    )

    model_pais_name: str = Field(
        default="gpt-4o-mini",
        alias="MODEL_PAIS_NAME",
        description="Modelo para a chain de país.",
    )
    model_pais_temp: float = Field(
        default=0.1,
        alias="MODEL_PAIS_TEMP",
        description="Temperatura para a chain de país.",
    )
    model_city_name: str = Field(
        default="gpt-4o-mini",
        alias="MODEL_CITY_NAME",
        description="Modelo para a chain de cidade.",
    )
    model_city_temp: float = Field(
        default=0.7,
        alias="MODEL_CITY_TEMP",
        description="Temperatura para a chain de cidade.",
    )

    model_config = SettingsConfigDict(
        env_file=find_dotenv(), env_file_encoding="utf-8", extra="ignore"
    )


# instancia (importe `settings` onde precisar)
settings = Settings()  # type: ignore


if __name__ == "__main__":
    print(settings)
