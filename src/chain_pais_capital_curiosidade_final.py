"""
Estudo de Pipeline LangChain: Países e Curiosidades
==================================================

Este script demonstra uma pipeline completa no LangChain, seguindo um fluxo
lógico e educacional para o aprendizado:

1.  SETUP: Configurações e definições iniciais.
2.  COMPONENTE 1: A primeira cadeia, que obtém dados estruturados de um país.
3.  COMPONENTE 2: A segunda cadeia, que obtém uma curiosidade sobre uma cidade.
4.  PIPELINE FINAL: A "cadeia-mãe" que conecta as duas partes em um fluxo único.
5.  EXECUÇÃO: O ponto de entrada que invoca a pipeline e exibe o resultado.

A chave é usar `RunnablePassthrough.assign()` para fazer a "ponte" entre as duas chains,
salvando o resultado da primeira para ser usado como entrada da segunda.
"""

# ============================================================
# 1. SETUP: CONFIGURAÇÃO E DEFINIÇÕES
# ============================================================
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# ✅ Carrega as configurações de um arquivo .env
_ = load_dotenv(find_dotenv())

class Settings(BaseSettings):
    """Configurações centralizadas do projeto."""
    openai_api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")

    class Config:
        env_file = find_dotenv()
        env_file_encoding = "utf-8"

settings = Settings()

# ✅ Definição do modelo de dados
class Pais(BaseModel):
    """Representa os dados estruturados de um país."""
    nome: str = Field(description="Nome do país")
    capital: str = Field(description="Capital do país")

# ✅ Instancia os modelos de linguagem com temperaturas específicas
model_info = ChatOpenAI(api_key=settings.openai_api_key.get_secret_value(), model="gpt-4o-mini", temperature=0.1)
model_curiosity = ChatOpenAI(api_key=settings.openai_api_key.get_secret_value(), model="gpt-4o-mini", temperature=0.7)


# ============================================================
# 2. COMPONENTE 1: Cadeia de Informações do País
# ============================================================
# ✅ Recebe um 'pais' e retorna um objeto 'Pais'
prompt_info = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que sabe informações sobre países."),
    ("user", "Qual é a capital do {pais}?")
])
chain_info = prompt_info | model_info.with_structured_output(Pais)


# ============================================================
# 3. COMPONENTE 2: Cadeia de Curiosidades da Cidade
# ============================================================
# ✅ Recebe uma 'cidade' e retorna uma curiosidade
prompt_curiosity = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que sabe informações sobre cidades."),
    ("user", "Diga uma curiosidade sobre a {cidade}")
])
chain_curiosity = prompt_curiosity | model_curiosity


# ============================================================
# 4. PIPELINE FINAL: Unindo os componentes em um fluxo único
# ============================================================
# ✅ A pipeline principal, que executa o fluxo completo do início ao fim
pipeline_final = (
    # Passo 1: Executa a primeira cadeia (chain_info) e salva o resultado
    #          no fluxo de dados com a chave 'pais_obj'
    RunnablePassthrough.assign(pais_obj=chain_info)

    # Passo 2: Executa a segunda cadeia (chain_curiosity). A entrada para esta
    #          cadeia é extraída do fluxo de dados existente (`x['pais_obj']`).
    #          O resultado é salvo na chave 'curiosity_city'.
    | RunnablePassthrough.assign(
        curiosity_city=RunnableLambda(lambda x: {"cidade": x["pais_obj"].capital})
        | chain_curiosity
    )

    # Passo 3: Formata a resposta final usando os resultados de ambos os passos
    | RunnableLambda(lambda x:
        f"--- Detalhes do País ---\n"
        f"Nome: {x['pais_obj'].nome}\n"
        f"Capital: {x['pais_obj'].capital}\n\n"
        f"--- Curiosidade da Cidade ---\n"
        f"{x['curiosity_city'].content}\n"
    )
)


# ============================================================
# 5. EXECUÇÃO DA PIPELINE
# ============================================================
if __name__ == "__main__":
    # ✅ Ponto de entrada: define a entrada inicial para a pipeline
    input_data = {"pais": "Suíça"}
    print(f"🚀 Iniciando a pipeline para o país: {input_data['pais']}")
    
    # ✅ Executa a pipeline
    resultado = pipeline_final.invoke(input_data)
    
    # ✅ Exibe o resultado final
    print("\n" + "="*50 + "\n")
    print(resultado)
    print("\n" + "="*50 + "\n")