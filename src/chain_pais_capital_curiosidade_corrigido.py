"""
Este script utiliza o langchain para criar uma chain que:
- Recebe o nome de um país
- Retorna a capital desse país
- Retorna uma curiosidade sobre a capital desse país

Configuração via Pydantic Settings:
- Validação automática de variáveis obrigatórias
- Tipagem forte (str, bool, etc.)
- Defaults claros para variáveis opcionais
"""

# ============================================================
# 1. IMPORTAÇÕES
# ============================================================
from dotenv import find_dotenv
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


# ============================================================
# 2. CONFIGURAÇÕES DO PROJETO (SETTINGS)
# ============================================================
class Settings(BaseSettings):
    """Configurações centralizadas do projeto."""

    # Variáveis obrigatórias
    openai_api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")
    langsmith_api_key: SecretStr = Field(..., alias="LANGSMITH_API_KEY")

    # Variáveis opcionais
    langsmith_tracing: bool = Field(False, alias="LANGSMITH_TRACING")
    langsmith_endpoint: str = Field("https://api.smith.langchain.com", alias="LANGSMITH_ENDPOINT")
    langsmith_project: str = Field("Default Project", alias="LANGSMITH_PROJECT")

    class Config:
        env_file = find_dotenv()
        env_file_encoding = "utf-8"

# Instancia as configurações no nível do módulo para carregar as variáveis de ambiente
# do .env antes que qualquer outro código que dependa delas seja executado.
settings = Settings()


# ============================================================
# 3. MODELOS DE DADOS
# ============================================================
class Pais(BaseModel):
    """Representa os dados estruturados de um país."""
    nome: str = Field(description="Nome do país")
    capital: str = Field(description="Capital do país")


# ============================================================
# 4. DEFINIÇÃO DAS CHAINS
# ============================================================

# --- Chain 1: Obter informações do país ---
model_pais = ChatOpenAI(
    api_key=settings.openai_api_key,  # Corrigido: passando SecretStr diretamente
    model="gpt-4o-mini",
    temperature=0.1
).with_structured_output(Pais)
prompt_pais = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que sabe informações sobre países."),
    ("user", "Qual é a capital do {pais}?")
])
chain_pais = prompt_pais | model_pais

# --- Chain 2: Obter curiosidade sobre cidade ---
model_city = ChatOpenAI(
    api_key=settings.openai_api_key,  # Corrigido: passando SecretStr diretamente
    model="gpt-4o-mini",
    temperature=0.7
)
prompt_city = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que sabe informações sobre cidades."),
    ("user", "Diga uma curiosidade sobre a {cidade}")
])
chain_city = prompt_city | model_city  # type: ignore

# --- Sub-chain: Conectar saída de Pais → entrada de City ---
sub_chain_city = (  # type: ignore
    RunnableLambda(lambda x: {"cidade": x["pais_obj"].capital})  # type: ignore
    | chain_city
)


# ============================================================
# 5. CHAIN PRINCIPAL (PIPELINE)
# ============================================================
final_chain = (  # type: ignore
    RunnablePassthrough.assign(pais_obj=chain_pais)  # type: ignore
    | RunnablePassthrough.assign(curiosity_city=sub_chain_city)  # type: ignore
    | RunnableLambda(lambda x:  # type: ignore
        f"--- Detalhes do País ---\n"
        f"Nome: {x['pais_obj'].nome}\n"  # type: ignore
        f"Capital: {x['pais_obj'].capital}\n\n"  # type: ignore
        f"--- Curiosidade da Cidade ---\n"
        f"{x['curiosity_city'].content}\n"  # type: ignore
    )
)


# ============================================================
# 6. PONTO DE ENTRADA (MAIN)
# ============================================================
if __name__ == "__main__":
    print("✅ Configurações carregadas:")
    print("OPENAI_API_KEY:", settings.openai_api_key.get_secret_value()[:4] + "..." + settings.openai_api_key.get_secret_value()[-4:])  # Corrigido: usando get_secret_value() com SecretStr
    print("LANGSMITH_API_KEY:", settings.langsmith_api_key.get_secret_value()[:4] + "..." + settings.langsmith_api_key.get_secret_value()[-4:])  # Corrigido: usando get_secret_value() com SecretStr
    print("LANGSMITH_PROJECT:", settings.langsmith_project)

    # Executar exemplo
    resultado = final_chain.invoke({"pais": "China"})
    print(resultado)
