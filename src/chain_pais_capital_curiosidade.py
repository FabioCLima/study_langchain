"""
Este script utiliza o langchain para criar uma chain que:
- Recebe o nome de um país
- Retorna a capital desse país
- Retorna uma curiosidade sobre a capital desse país

Criando uma configuração do projeto utilizando Pydantic:
 -- Validação automática de variáveis obrigatórias
 -- Tipagem forte (str, bool, etc.)
 -- Default claros para variáveis opcionais.
"""

#! Importações necessárias
from dotenv import find_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# * Class Settings para configuração do projeto
class Settings(BaseSettings):
    """
    Classe de configuração centralizada.
    Pydantic v2 usa o pacote pydantic-settings para BaseSettings.
    """

    # 🔑 Variáveis obrigatórias
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    langsmith_api_key: str = Field(..., alias="LANGSMITH_API_KEY")

    # 🔧 Variáveis opcionais
    langsmith_tracing: bool = Field(False, alias="LANGSMITH_TRACING")
    langsmith_endpoint: str = Field(
        "https://api.smith.langchain.com", alias="LANGSMITH_ENDPOINT"
    )
    langsmith_project: str = Field("Default Project", alias="LANGSMITH_PROJECT")

    # 🔽 Essa classe interna é o "cérebro" de configuração da Settings
    class Config:
        # Diz ao Pydantic onde procurar variáveis
        env_file = find_dotenv()  # procura automaticamente pelo .env
        env_file_encoding = (
            "utf-8"  # garante que acentos/caracteres especiais sejam lidos corretamente
        )


#! Resolvendo o problema proposto:
#! ---- PASSO 1: DEFINIR MODELOS DE DADOS ESTRUTURADOS ----
#! Sempre comece definindo as estruturas de dados que serão usadas
class Pais(BaseModel):
    """Representa os dados estruturados de um país.

    Attributes:
        nome: O nome do país.
        capital: A capital do país.
    """
    nome: str = Field(description="Nome do país")
    capital: str = Field(description="Capital do país")

#! ---- PASSO 2: CRIAR CHAINS INDIVIDUAIS COM RESPONSABILIDADES ESPECÍFICAS ----
#! Cada chain deve ter uma responsabilidade bem definida e retornar dados
#!consistente
#* Chain1 - Obter informações estruturadas sobre um país
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)   

prompt_pais = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que sabe informações sobre países."),
    ("user", "Qual é a capital do {pais}?")
])

#! Usar .with_structured_output() para garantir dados estruturados
model_pais = model.with_structured_output(Pais)
chain_pais = prompt_pais | model_pais

#* Chain2 - Obter curiosidades sobre uma cidade
model_city = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
prompt_city = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que sabe informações sobre cidades."),
    ("user", "Diga uma curiosidade sobre a {cidade}")
])

chain_city = prompt_city | model_city

#* Aqui para ficar registrado, da chain obtemos o nome da capital do país
#* E usamos essa string para obter a curiosidade sobre a capital do país
#* A saída da primeira chain é um objeto pydantic Pais, que deve ser
#* transformado em um dicionário para ser usado na segunda chain
#* Sempre procurar entender a estrutura de dados para saber como conectar as 
#* chains sem perder os dados que são necessários para a cadeia de processo

#! ---- PASSO 3: CRIAR SUB-CHAINS DE TRANSFORMAÇÃO ----
#! Sub-chains fazem a ponte entre diferentes formatos de dados
#! PROBLEMA: chain_pais retorna objeto Pais, mas chain_city espera
# !{"cidade": "valor"}
sub_chain_city = (
    #* TRANSFORMAÇÃO: De objeto Pais para dicionário {"cidade": capital}
    #* x["pais_obj"] é o objeto Pais retornado pela chain_pais
    #* x["pais_obj"].capital extrai o atributo capital
    RunnableLambda(lambda x: {"cidade": x["pais_obj"].capital})
    | chain_city  #* Esta chain espera {"cidade": "valor"}
)

#! ---- PASSO 4: CONSTRUIR CHAIN PRINCIPAL SEQUENCIAL ----
#* ARQUITETURA: Cada etapa ADICIONA dados ao fluxo usando RunnablePassthrough.assign()

final_chain = (
    #* ETAPA 1: Obter dados do país e ADICIONAR ao fluxo
    #* Entrada: {"pais": "Suíça"}
    #* Saída: {"pais": "Suíça", "pais_obj": <objeto_Pais>}
    RunnablePassthrough.assign(pais_obj=chain_pais)
    
    #* ETAPA 2: Obter curiosidade da capital e ADICIONAR ao fluxo
    #* Entrada: {"pais": "Suíça", "pais_obj": <objeto_Pais>}
    #* Saída: {"pais": "Suíça", "pais_obj": <objeto_Pais>, "curiosity_city": <AIMessage>}
    | RunnablePassthrough.assign(curiosity_city=sub_chain_city)
    
    #* ETAPA 3: Formatar resultado final usando TODOS os dados coletados
    #* Entrada: Dicionário completo com todas as chaves
    #* Saída: String formatada com informações consolidadas
    | RunnableLambda(lambda x: 
        f"--- Detalhes do Pais ---\n"
        f"Nome: {x['pais_obj'].nome}\n"
        f"Capital: {x['pais_obj'].capital}\n\n"
        f"--- Curiosidade da Cidade ---\n"
        f"{x['curiosity_city'].content}\n"
    )
)

#! ---- PASSO 5: EXECUTAR E TESTAR ----
#! Sempre teste com dados simples primeiro
resultado_final = final_chain.invoke({"pais": "Paris"})
print(resultado_final)
# 🚀 Teste rápido
if __name__ == "__main__":
    #! ---- PASSO 0: CARREGAR CONFIGURAÇÕES ----
    #! Carrega variáveis automaticamente do .env
    settings = Settings()
    
    print("✅ Configurações carregadas:")
    print("OPENAI_API_KEY:", settings.openai_api_key[:10] + "...")
    print("LANGSMITH_API_KEY:", settings.langsmith_api_key[:10] + "...")
    print("LANGSMITH_PROJECT:", settings.langsmith_project)
    print("LANGSMITH_TRACING:", settings.langsmith_tracing)
    print("LANGSMITH_ENDPOINT:", settings.langsmith_endpoint)
