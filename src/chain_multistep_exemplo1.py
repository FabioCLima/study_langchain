# -*- coding: utf-8 -*-
"""
Solução refatorada para o exercício de Workflow Multi-Etapas,
aplicando as melhores práticas atuais do LangChain (LCEL).

- Fluxo de dados explícito entre as chains.
- Nomenclatura clara.
- Cadeia de ponta a ponta (e2e) robusta.
"""

import os
from operator import itemgetter
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from pydantic import BaseModel, Field

# --- 1. CONFIGURAÇÃO INICIAL E DO MODELO ---
# Carrega a chave da API do arquivo .env (boa prática de segurança)
_ = load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no .env")

# Instancia o modelo com temperatura baixa para respostas mais focadas
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
)

# --- 2. LOGGING INTELIGENTE E PARSER (MANTIDO COMO BOA PRÁTICA) ---
# Lista para armazenar o histórico de chamadas brutas ao LLM para depuração
logs = []
# Parser padrão para extrair o texto da resposta do LLM
parser = StrOutputParser()

# Esta cadeia paralela é uma excelente prática. Ela faz duas coisas ao mesmo tempo:
# 1. 'output': Fornece o texto limpo e parseado.
# 2. 'log': Salva a mensagem bruta do modelo (AIMessage) na nossa lista de logs.
parse_and_log_output_chain = RunnableParallel(
    output=parser,
    log=RunnableLambda(lambda x: logs.append(x))
)

# --- 3. DEFINIÇÃO DAS ETAPAS MODULARES ---

# ETAPA 1: GERAÇÃO DA IDEIA
# Espera um dicionário de entrada: {"industry": "..."}
idea_prompt = PromptTemplate.from_template(
    "You are a creative business advisor. "
    "Generate one innovative business idea in the industry: {industry}. "
    "Provide a brief description of the idea."
)
idea_chain = idea_prompt | llm | parse_and_log_output_chain

# ETAPA 2: ANÁLISE DA IDEIA
# Espera um dicionário de entrada: {"idea": "..."}
analysis_prompt = PromptTemplate.from_template(
    "Analyze the following business idea: "
    "Idea: {idea} "
    "Identify 3 key strengths and 3 potential weaknesses of the idea."
)
analysis_chain = analysis_prompt | llm | parse_and_log_output_chain

# ETAPA 3: GERAÇÃO DO RELATÓRIO ESTRUTURADO
# Define a estrutura de saída desejada usando Pydantic. Isso garante dados confiáveis.
class AnalysisReport(BaseModel):
    """Strengths and Weaknesses about a business idea."""
    strengths: list[str] = Field(description="List of the idea's strengths.")
    weaknesses: list[str] = Field(description="List of the idea's weaknesses.")

# Espera um dicionário de entrada: {"analysis_text": "..."}
report_prompt = PromptTemplate.from_template(
    "Based on the following business analysis, generate a structured report.\n"
    "Analysis: {analysis_text}"
)

# A melhor prática para saída estruturada: .with_structured_output()
# Ele cuida de instruir o modelo para retornar um JSON no formato da classe Pydantic.
report_chain = report_prompt | llm.with_structured_output(schema=AnalysisReport)


# --- 4. A CHAIN DE PONTA A PONTA (VERSÃO MELHORADA E ROBUSTA) ---
# Esta é a principal melhoria, corrigindo o "vício" do código original.
# O fluxo de dados entre as etapas é explícito e garantido.
e2e_chain = (
    # A entrada inicial para a cadeia é {"industry": "..."}
    idea_chain
    # A saída da 'idea_chain' é {'output': str, 'log': AIMessage}.
    # A 'analysis_chain' espera {'idea': str}.
    # Usamos 'itemgetter' para pegar o valor de 'output' e colocá-lo na chave 'idea'.
    | RunnableParallel(idea=itemgetter("output"))
    # Agora, o dado é {'idea': '...texto da ideia...'}. Perfeito para a próxima etapa.
    | analysis_chain
    # A saída da 'analysis_chain' é {'output': str, 'log': AIMessage}.
    # A 'report_chain' espera {'analysis_text': str}.
    # Fazemos a mesma transformação de dados.
    | RunnableParallel(analysis_text=itemgetter("output"))
    # Agora, o dado é {'analysis_text': '...texto da análise...'}.
    | report_chain
)

# --- 5. EXECUÇÃO ---
if __name__ == "__main__":
    print("🚀 Executando a cadeia de ponta a ponta melhorada...")

    # A entrada é um dicionário, conforme esperado pela primeira 'chain'
    final_report = e2e_chain.invoke({"industry": "ecoturismo na chapada dos veadeiros"})

    print("\n" + "="*50)
    print("📄 Relatório Final Estruturado Gerado")
    print("="*50)
    print(f"✅ Pontos Fortes: {final_report.strengths}")
    print(f"⚠️ Pontos Fracos:  {final_report.weaknesses}")
    print("="*50)

    # Opcional: Inspecionar os logs para depuração
    print(f"\n📚 Foram registradas {len(logs)} chamadas ao LLM.")
    # print("Logs brutos:", logs)