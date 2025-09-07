import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)
from langchain_openai import ChatOpenAI

# ! TODO - Instantiate your chat model
# * Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# * Verifica se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

# * Configura o modelo com parâmetros específicos
model: ChatOpenAI = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.0,  # Controla a criatividade das respostas
)  # type: ignore


# * Funçòes simples para demonstrar
def contar_palavras(texto: str) -> int:
    """Conta quantas palavras tem no texto"""
    return len(texto.split())


def contar_caracteres(texto: str) -> int:
    """Conta quantos caracteres tem no texto"""
    return len(texto)


def converter_maiusculo(texto: str) -> str:
    """Converte texto para maiúsculo"""
    return texto.upper()


# * 2. Criando um RunnableParallel
# * Isso executa TRÊS operações em paralelo!
analisador_paralelo = RunnableParallel(
    palavras=RunnableLambda(contar_palavras),
    caracteres=RunnableLambda(contar_caracteres),
    maiusculo=RunnableLambda(converter_maiusculo)
)
# * 3. Testando nosso RunnableParallel
texto_teste = "Olá mundo! Como você está?"

print("=== TESTE DO RUNNABLEPARALLEL ===")
print(f"Texto de entrada: '{texto_teste}'")
print()

resultado = analisador_paralelo.invoke(texto_teste)

print("Resultado (execução paralela):")
print(f"- Palavras: {resultado['palavras']}")
print(f"- Caracteres: {resultado['caracteres']}")
print(f"- Maiúsculo: '{resultado['maiusculo']}'")

# 4. Comparando com execução sequencial
print("\n=== COMPARAÇÃO COM EXECUÇÃO SEQUENCIAL ===")
print("Se fizéssemos uma após a outra:")
print(f"- Palavras: {contar_palavras(texto_teste)}")
print(f"- Caracteres: {contar_caracteres(texto_teste)}")
print(f"- Maiúsculo: '{converter_maiusculo(texto_teste)}'")

# * 5. Exemplo mais complexo - combinando com outros componentes

# * Prompt para gerar um resumo
prompt_resumo = PromptTemplate(
    template="Faça um resumo de 2 frases sobre: {texto}",
    input_variables=["texto"]
)

# * Prompt para gerar palavras-chave
prompt_palavras_chave = PromptTemplate(
    template="Extraia 3 palavras-chave de: {texto}",
    input_variables=["texto"]
)

# * RunnableParallel mais complexo
analisador_avancado = RunnableParallel(
    resumo=prompt_resumo | StrOutputParser(),
    palavras_chave=prompt_palavras_chave | StrOutputParser(),
    estatisticas=RunnableParallel(
        palavras=RunnableLambda(contar_palavras),
        caracteres=RunnableLambda(contar_caracteres)
    )
)

print("\n=== EXEMPLO AVANÇADO ===")
texto_avancado = "A inteligência artificial está revolucionando a forma como trabalhamos e vivemos no século XXI."

# * Nota: Este exemplo precisaria de um LLM real para funcionar
# * resultado_avancado = analisador_avancado.invoke({"texto": texto_avancado})
print("Este exemplo mostra como combinar prompts, parsers e funções em paralelo!")
