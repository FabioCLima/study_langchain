"""Exercício1: O Crítico culinário
Objetivo é praticar a conexão de duas chain que não tem formato de entrada e saída,
compatíveis, exigindo um "adaptador" - "RunnableLambda"

crie uma `chain_pratos` que recebe um `País` e lista 3 práticos típicos do país.
input = {"país": 'Itália'
output_expected = []
"""

from contextlib import redirect_stdout
from io import StringIO

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from openai_client import create_analytical_model

# * Sem logs de debug ou print
with redirect_stdout(StringIO()):
    model: ChatOpenAI | None = create_analytical_model()


if model is None:
    print("❌ Erro: Não foi possível criar o modelo OpenAI.")
    print("💡 Certifique-se de que:")
    print("   1. Existe um arquivo .env no diretório src/")
    print("   2. O arquivo .env contém: OPENAI_API_KEY=sua_chave_aqui")
    print("   3. A chave da API é válida")
    exit(1)

parser = StrOutputParser()

# * 1.Chains individuais:
prompt_pratos = ChatPromptTemplate.from_template(
    "Liste 3 pratos típicos do seguinte país: {pais}"
)
chain_pratos = prompt_pratos | model | parser  # type: ignore


prompt_descricao = ChatPromptTemplate.from_template(
    """Descreve o prato '{nome_do_prato}' de forma curta e apetitosa."""
)
chain_descricao = prompt_descricao | model | parser  # type: ignore


# * 2.Função para extrair o primeiro prato
def extrair_primeiro_prato(texto_lista: str) -> str:
    """Extrai o nome do primeiro prato da lista retornada pelo modelo."""
    linhas = texto_lista.strip().split("\n")
    if not linhas:
        return "Prato não encontrado"

    primeira_linha = linhas[0]
    # Remove "1. ", "1- ", "1) " etc
    for separador in [". ", "- ", ") "]:
        if separador in primeira_linha:
            return primeira_linha.split(separador, 1)[1]

    # Se não encontrar separador, retorna a linha completa
    return primeira_linha


# 3. Chain combinada
chain_final = (  # type: ignore
    chain_pratos
    | RunnableLambda(extrair_primeiro_prato)
    | (lambda nome: {"nome_do_prato": nome})  # type: ignore # Outro lambda para formatar o dicionário
    | chain_descricao
)

print("\n--- Exercício 1: Crítico Culinário ---")
print(chain_final.invoke({"pais": "Japão"}))  # type: ignore
