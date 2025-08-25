"""
Protótipo de Estudo LangChain: Encadeamento de Informações de Países
===================================================================

Este script demonstra a criação de uma pipeline de duas etapas, focando
nos conceitos de encadeamento com RunnablePassthrough.assign().
"""

import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from pydantic import BaseModel, Field

# ============================================================
# 1. CONFIGURAÇÃO BÁSICA
# ============================================================

# ✅ Usa o python-dotenv para carregar as variáveis de ambiente do arquivo .env
_ = load_dotenv(find_dotenv())

# ✅ Acessa a variável de ambiente, garantindo que ela existe
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "A variável de ambiente 'OPENAI_API_KEY' não está definida."
        "Crie um arquivo .env na raiz do projeto com OPENAI_API_KEY='sua_chave_aqui'"
    )

# ============================================================
# 2. MODELOS DE DADOS E LANGCHAIN
# ============================================================

# ✅ O modelo Pydantic para saída estruturada
class CountryInfo(BaseModel):
    """Modelo para informações estruturadas de um país."""
    nome: str = Field(description="Nome oficial do país")
    capital: str = Field(description="Capital do país")

# ✅ Criação dos modelos de linguagem
# Use um para cada tipo de tarefa, conforme a sua necessidade de 'temperature'
model_structured = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=OPENAI_API_KEY)
model_creative = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=OPENAI_API_KEY)


# ============================================================
# 3. CONSTRUÇÃO DOS COMPONENTES (CADEIAS)
# ============================================================

# ✅ Primeira Cadeia: Obtém a informação do país (Saída estruturada)
country_chain = (
    ChatPromptTemplate.from_messages([
        ("system", 
         "Você é um especialista em geografia mundial. Forneça informações precisas."),
        ("user", "Qual é a capital de {pais}?")
    ])
    | model_structured.with_structured_output(CountryInfo)
)

# ✅ Segunda Cadeia: Obtém uma curiosidade (Saída de texto)
curiosity_chain = (
    ChatPromptTemplate.from_messages([
        ("system", 
         "Você é um guia turístico. Conte curiosidades interessantes, verídicas e pouco conhecidas."),
        ("user", "Conte uma curiosidade fascinante sobre {cidade}")
    ])
    | model_creative
)

# ============================================================
# 4. MONTAGEM DA PIPELINE COMPLETA
# ============================================================

# ✅ A "cola" para a segunda cadeia: extrai a capital e a passa para o prompt seguinte
# Isso só precisa de um RunnableLambda, como no nosso último exercício
capital_to_curiosity = RunnableLambda(lambda x: {"cidade": x.capital}) | curiosity_chain

# ✅ A pipeline principal: usa RunnablePassthrough.assign para combinar os resultados
pipeline = (
    # Adiciona o resultado da primeira cadeia ao fluxo
    RunnablePassthrough.assign(country_info=country_chain)
    # Usa o resultado da primeira cadeia para executar a segunda
    | RunnablePassthrough.assign(curiosity=capital_to_curiosity)
    # Formata a resposta final, usando as duas saídas
    | RunnableLambda(lambda x: 
        f"🌍 Detalhes: {x['country_info'].nome} - Capital: {x['country_info'].capital}\n"
        f"✨ Curiosidade: {x['curiosity'].content}"
    )
)


# ============================================================
# 5. EXECUÇÃO DA PIPELINE
# ============================================================

# ✅ Executa a pipeline com uma entrada
nome_pais = "Japão"
print(f"🚀 Consultando informações e curiosidade sobre {nome_pais}...")
resultado_final = pipeline.invoke({"pais": nome_pais})

print("\n" + "="*50 + "\n")
print(resultado_final)
print("\n" + "="*50 + "\n")