# Exemplo Didático: RunnableParallel
# Vamos entender como funciona o RunnableParallel passo a passo

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel


# 1. Funções simples para demonstrar
def contar_palavras(texto):
    """Conta quantas palavras tem no texto"""
    return len(texto.split())


def contar_caracteres(texto):
    """Conta quantos caracteres tem no texto"""
    return len(texto)


def converter_maiusculo(texto):
    """Converte texto para maiúsculo"""
    return texto.upper()


# 2. Criando um RunnableParallel
# Isso executa TRÊS operações em paralelo!
analisador_paralelo = RunnableParallel(
    palavras=RunnableLambda(contar_palavras),
    caracteres=RunnableLambda(contar_caracteres),
    maiusculo=RunnableLambda(converter_maiusculo)
)

# 3. Testando nosso RunnableParallel
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

# 5. Exemplo mais complexo - combinando com outros componentes
from langchain_core.prompts import PromptTemplate

# Prompt para gerar um resumo
prompt_resumo = PromptTemplate(
    template="Faça um resumo de 2 frases sobre: {texto}",
    input_variables=["texto"]
)

# Prompt para gerar palavras-chave
prompt_palavras_chave = PromptTemplate(
    template="Extraia 3 palavras-chave de: {texto}",
    input_variables=["texto"]
)

# RunnableParallel mais complexo
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

# Nota: Este exemplo precisaria de um LLM real para funcionar
# resultado_avancado = analisador_avancado.invoke({"texto": texto_avancado})
print("Este exemplo mostra como combinar prompts, parsers e funções em paralelo!")
