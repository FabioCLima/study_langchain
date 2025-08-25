"""
Exercício Didático: Pipeline de Ideias com LangChain

Objetivo: Criar um pipeline onde a primeira chain gera uma lista de ideias
e a segunda chain seleciona e reformula a melhor ideia em um formato estruturado.

Conceitos praticados:
- Composição de chains com o operador pipe (`|`).
- Uso de `RunnableLambda` para transformar dados entre as etapas.
- Geração de saída estruturada com Pydantic e `.with_structured_output()`.
- Boas práticas de código: funções modulares e clareza.
"""
import os
import re
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

# --- 1. CONFIGURAÇÃO INICIAL ---
# Carrega a chave da API e instancia o modelo
load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no .env")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# --- 2. DEFINIÇÃO DO FORMATO DE SAÍDA (A "MELHOR FORMATAÇÃO") ---
# Usamos Pydantic para garantir que a saída final seja sempre um objeto
# estruturado, previsível e fácil de usar no resto do seu código.
class IdeiaReformulada(BaseModel):
    """Define a estrutura de uma ideia de negócio bem formatada."""
    nome_ideia: str = Field(description="Um nome criativo e curto para a ideia.")
    pitch: str = Field(description="Uma frase de efeito (pitch) que resume a ideia.")
    publico_alvo: str = Field(description="O público-alvo principal para esta ideia.")

# --- 3. CRIAÇÃO DAS CHAINS MODULARES ("LEGO BLOCKS") ---

# Bloco 1: Gerador de Ideias
# Esta chain recebe um tema e retorna uma string com uma lista de ideias.
prompt_ideias = ChatPromptTemplate.from_template(
    "Você é um consultor de inovação. Gere 3 ideias de negócio criativas e distintas "
    "baseadas no seguinte tema: {tema}. Liste-as numericamente."
)
chain_ideias = prompt_ideias | model | StrOutputParser()

# Bloco 2: Reformulador de Ideia
# Esta chain recebe UMA ideia bruta e a transforma no nosso modelo Pydantic.
# O `.with_structured_output()` é a mágica aqui. Ele instrui o LLM a
# formatar sua resposta para corresponder exatamente à classe `IdeiaReformulada`.
prompt_reformulacao = ChatPromptTemplate.from_template(
    "Você é um especialista em marketing. Pegue a seguinte ideia de negócio bruta e "
    "a reformule em um formato mais atraente. \n\n"
    "Ideia Bruta: {ideia_bruta}"
)
chain_reformulacao = prompt_reformulacao | model.with_structured_output(IdeiaReformulada)

# --- 4. O "ADAPTADOR": A FUNÇÃO QUE CONECTA AS CHAINS ---
# A `chain_ideias` retorna uma string com 3 ideias. A `chain_reformulacao`
# espera uma única ideia. Esta função faz a "ponte" entre elas.
def extrair_primeira_ideia(texto_com_lista: str) -> str:
    """
    Extrai a primeira ideia de uma lista de texto numerada.
    É robusta o suficiente para lidar com formatos como '1. ' ou '1- '.
    """
    # Tenta encontrar a primeira linha que começa com um número, ponto ou traço.
    match = re.search(r"^\s*(?:1\.|1-|\*)\s*(.*)", texto_com_lista, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Se não encontrar um padrão, retorna a primeira linha não vazia como fallback.
    primeira_linha = next((line for line in texto_com_lista.strip().split('\n') if line.strip()), None)
    return primeira_linha if primeira_linha else "Nenhuma ideia encontrada."


# --- 5. MONTAGEM DO PIPELINE FINAL ---
# Agora, conectamos tudo com o operador pipe (`|`).
# O fluxo de dados é explícito e fácil de ler.
pipeline_completo = (
    chain_ideias
    # A saída de `chain_ideias` (uma string) é passada para nossa função adaptadora.
    | RunnableLambda(extrair_primeira_ideia)
    # A saída da função (uma string com uma ideia) precisa ser formatada em um
    # dicionário `{"ideia_bruta": "..."}` para a `chain_reformulacao`.
    # Outro `RunnableLambda` é perfeito para essa pequena transformação.
    | RunnableLambda(lambda ideia_texto: {"ideia_bruta": ideia_texto})
    # O dicionário formatado é finalmente passado para a chain de reformulação.
    | chain_reformulacao
)

# --- 6. EXECUÇÃO E EXIBIÇÃO ---
def exibir_resultado(ideia: IdeiaReformulada):
    """Formata a saída do Pydantic de uma forma amigável."""
    print("\n" + "💡" * 20)
    print("    IDEIA DE NEGÓCIO REFINADA")
    print("💡" * 20)
    print(f"🏷️ Nome: {ideia.nome_ideia}")
    print(f"🚀 Pitch: {ideia.pitch}")
    print(f"🎯 Público-alvo: {ideia.publico_alvo}")
    print("💡" * 20)


if __name__ == "__main__":
    print("🚀 Iniciando pipeline para gerar e refinar uma ideia de negócio...")
    tema_usuario = "cafeterias com tema de tecnologia"

    # `invoke` executa toda a cadeia de ponta a ponta
    resultado_final = pipeline_completo.invoke({"tema": tema_usuario})

    exibir_resultado(resultado_final)
