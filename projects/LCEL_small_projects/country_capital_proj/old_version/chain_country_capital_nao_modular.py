"""Este script utiliza o langchain para criar uma chain que:
- Recebe o nome de um país
- Retorna a capital desse país
- Retorna uma curiosidade sobre a capital desse país

Configuração via Pydantic Settings:
- Validação automática de variáveis obrigatórias
- Tipagem forte (str, bool, etc.)
- Defaults claros para variáveis opcionais
"""

# ! ============================================================
# ! 1. IMPORTAÇÕES
# ! ============================================================

import argparse
from collections.abc import Mapping
from typing import Any

from dotenv import find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings


# ! ============================================================
# ! 2. CONFIGURAÇÕES DO PROJETO (SETTINGS)
# ! ============================================================
class Settings(BaseSettings):
    """Configurações centralizadas do projeto."""

    # * Variáveis obrigatórias
    openai_api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")
    langsmith_api_key: SecretStr = Field(..., alias="LANGSMITH_API_KEY")

    # * Variáveis opcionais
    langsmith_tracing: bool = Field(False, alias="LANGSMITH_TRACING")
    langsmith_endpoint: str = Field(
        "https://api.smith.langchain.com", alias="LANGSMITH_ENDPOINT"
    )
    langsmith_project: str = Field("Default Project", alias="LANGSMITH_PROJECT")

    # * Configuração de modelo LLM
    model_pais_name: str = Field("gpt-4o-mini", alias="MODEL_PAIS_NAME")
    model_pais_temp: float = Field(0.1, alias="MODEL_PAIS_TEMP")
    model_city_name: str = Field("gpt-4o-mini", alias="MODEL_CITY_NAME")
    model_city_temp: float = Field(0.7, alias="MODEL_CITY_TEMP")

    class Config:
        env_file = find_dotenv()
        env_file_encoding = "utf-8"


settings = Settings()


# ! ============================================================
# ! 3. MODELOS DE DADOS
# ! ============================================================
class Pais(BaseModel):
    """Representa os dados estruturados de um país."""

    nome: str = Field(description="Nome do país")
    capital: str = Field(description="Capital do país")


class Curiosidade(BaseModel):
    """Representa uma curiosidade sobre uma cidade."""

    curiosidade: str = Field(description="Curiosidade sobre a cidade")


class ResultadoFinal(BaseModel):
    """Modelo de saída final da pipeline."""

    pais: str = Field(description="Nome do país")
    capital: str = Field(description="Capital do país")
    curiosidade: str = Field(description="Curiosidade sobre a capital")


# ! ============================================================
# ! 4. DEFINIÇÃO DAS CHAINS
# ! ============================================================

# * --- Chain 1: Obter informações do país ---
model_pais = ChatOpenAI(
    api_key=settings.openai_api_key.get_secret_value(),
    model=settings.model_pais_name,
    temperature=settings.model_pais_temp,
).with_structured_output(Pais)

prompt_pais = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente que sabe informações sobre países."),
        ("user", "Qual é a capital do {pais}?"),
    ]
)
chain_pais = prompt_pais | model_pais

# * --- Chain 2: Obter curiosidade sobre cidade ---
model_city = ChatOpenAI(
    api_key=settings.openai_api_key.get_secret_value(),
    model=settings.model_city_name,
    temperature=settings.model_city_temp,
).with_structured_output(Curiosidade)

prompt_city = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente que sabe informações sobre cidades."),
        (
            "user",
            "Responda APENAS em JSON com a chave 'curiosidade'. "
            "Diga uma curiosidade curta sobre a cidade {cidade}.",
        ),
    ]
)

chain_city = prompt_city | model_city


# * --- Sub-chain: Conectar saída de Pais → entrada de City ---
def extract_city_from_country(data: Mapping[str, Any]) -> dict:
    """Extrai a cidade (capital) do país para passar como entrada na chain da cidade.

    Args:
        data: Dicionário contendo a chave 'pais_obj' com instância de Pais.

    Returns:
        dict: {"cidade": <capital>}

    """
    return {"cidade": data["pais_obj"].capital}


def build_final_result(data: Mapping[str, Any]) -> ResultadoFinal:
    """Monta a saída final estruturada da pipeline.

    Args:
        data: Dicionário contendo 'pais_obj' (Pais) e 'curiosity_city' (Curiosidade).

    Returns:
        ResultadoFinal: Saída estruturada com país, capital e curiosidade.

    """
    return ResultadoFinal(
        pais=data["pais_obj"].nome,
        capital=data["pais_obj"].capital,
        curiosidade=data["curiosity_city"].curiosidade,
    )


sub_chain_city = RunnableLambda(extract_city_from_country) | chain_city

# ! ============================================================
# ! 5. CHAIN PRINCIPAL (PIPELINE)
# ! ============================================================
final_chain = (
    RunnablePassthrough.assign(pais_obj=chain_pais)
    | RunnablePassthrough.assign(curiosity_city=sub_chain_city)
    | RunnableLambda(build_final_result)
)

# ! ============================================================
# ! 6. PONTO DE ENTRADA (MAIN)
# ! ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Obter capital e curiosidade de um país"
    )
    parser.add_argument("--pais", type=str, required=True, help="Nome do país")
    args = parser.parse_args()

    print("✅ Configurações carregadas:")
    print(
        "OPENAI_API_KEY:",
        settings.openai_api_key.get_secret_value()[:4]
        + "..."
        + settings.openai_api_key.get_secret_value()[-4:],
    )
    print(
        "LANGSMITH_API_KEY:",
        settings.langsmith_api_key.get_secret_value()[:4]
        + "..."
        + settings.langsmith_api_key.get_secret_value()[-4:],
    )
    print("LANGSMITH_PROJECT:", settings.langsmith_project)

    # Executar pipeline
    resultado: ResultadoFinal = final_chain.invoke({"pais": args.pais})  # type: ignore

    # Saída formatada
    print("\n📌 Resultado Final:")
    print(f"País       : {resultado.pais}")
    print(f"Capital    : {resultado.capital}")
    print(f"Curiosidade: {resultado.curiosidade}")
