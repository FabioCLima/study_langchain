"""Composição de chains com LangChain - Versão de Estudo"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI

# Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Verifica se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

# Configura o modelo
model = ChatOpenAI(model="gpt-4.1", temperature=0.1)  # type: ignore

# Prompt simples
prompt = PromptTemplate(
    template="Explique {tecnologia} em uma linha:",
    input_variables=["tecnologia"]
)

output_parser = StrOutputParser()

# Lista para capturar logs
logs = []


# Função simples para logar
def logar_operacao(x):  # type: ignore
    """Loga a operação atual"""
    logs.append(f"Operação: {x}")  # type: ignore
    return x


print("=" * 50)
print("1. CHAIN SIMPLES (sem logging)")
print("=" * 50)

# Chain básica
chain_simples = prompt | model | output_parser  # type: ignore
resultado_simples = chain_simples.invoke({"tecnologia": "Python"})  # type: ignore
print(f"Resultado: {resultado_simples}")

print("\n" + "=" * 50)
print("2. CHAIN COM RUNNABLELAMBDA (logging simples)")
print("=" * 50)

# Chain com RunnableLambda para logging
chain_com_log = prompt | model | RunnableLambda(logar_operacao) | output_parser  # type: ignore
resultado_com_log = chain_com_log.invoke({"tecnologia": "Docker"})  # type: ignore
print(f"Resultado: {resultado_com_log}")
print(f"Logs: {logs}")

print("\n" + "=" * 50)
print("3. CHAIN COM RUNNABLEPARALLEL (duas operações)")
print("=" * 50)

# Limpa logs para nova demonstração
logs.clear()

# RunnableParallel: executa parser E logging ao mesmo tempo
chain_paralela = prompt | model | RunnableParallel(
    output=output_parser,
    log=RunnableLambda(logar_operacao)  # type: ignore
)  # type: ignore

resultado_paralelo = chain_paralela.invoke({"tecnologia": "Kubernetes"})  # type: ignore
print(f"Resultado: {resultado_paralelo}")
print(f"Logs: {logs}")

print("\n" + "=" * 50)
print("CONCEITOS APRENDIDOS:")
print("=" * 50)
print("• RunnableLambda: Função customizada na chain")
print("• RunnableParallel: Executa operações independentes")
print("• Composição: prompt | model | parser")
print("• Side effects: Modificar variáveis durante execução")
